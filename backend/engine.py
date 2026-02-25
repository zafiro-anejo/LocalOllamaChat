from pathlib import Path
from typing import Optional

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    get_response_synthesizer,
    Settings,
)
from llama_index.core.retrievers import (
    VectorIndexRetriever,
    QueryFusionRetriever,
)
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.postprocessor import LLMRerank
from llama_index.vector_stores.qdrant import QdrantVectorStore

import config
from models import setup_models
from qdrant_utils import initialize_qdrant
from index_builder import build_index

class RAGEngine:
    def __init__(self, source_dir: Path, rebuild_if_exists: bool = False):
        self.source_dir = Path(source_dir)
        self.rebuild_if_exists = rebuild_if_exists
        setup_models()
        self.index: Optional[VectorStoreIndex] = None
        self.query_engine: Optional[RetrieverQueryEngine] = None
        self._initialize()

    def _initialize(self):
        if not self.source_dir.exists() or not any(self.source_dir.glob("*.md")):
            raise FileNotFoundError(f"[ERROR] No .md files in {self.source_dir}")

        qdrant_client = initialize_qdrant(self.rebuild_if_exists)
        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name=config.COLLECTION_NAME
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        if not self.rebuild_if_exists and qdrant_client.collection_exists(config.COLLECTION_NAME):
            try:
                self.index = VectorStoreIndex.from_vector_store(
                    vector_store,
                    storage_context=storage_context
                )
                print("[WARNING] Index loaded from Qdrant. Docstore is empty, BM25 will use empty node list.")
            except Exception as e:
                print(f"[ERROR] Failed to load index: {e}, creating new one.")
                self.index = build_index(storage_context, self.source_dir)
        else:
            self.index = build_index(storage_context, self.source_dir)

        vector_retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=config.SIMILARITY_TOP_K
        )

        nodes_for_bm25 = list(self.index.docstore.docs.values()) if self.index.docstore.docs else []
        if not nodes_for_bm25:
            print("[WARNING] Docstore is empty, BM25Retriever will return empty results.")
        bm25_retriever = BM25Retriever.from_defaults(
            nodes=nodes_for_bm25,
            similarity_top_k=config.SIMILARITY_TOP_K
        )

        hybrid_retriever = QueryFusionRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            similarity_top_k=config.HYBRID_TOP_K,
            num_queries=1,
            use_async=False,
            verbose=False
        )

        reranker = LLMRerank(
            choice_batch_size=5,
            top_n=config.RERANK_TOP_N
        )

        response_synthesizer = get_response_synthesizer(
            response_mode=ResponseMode.COMPACT,
            llm=Settings.llm
        )

        self.query_engine = RetrieverQueryEngine(
            retriever=hybrid_retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[reranker]
        )

    def ask(self, question: str) -> str:
        if not self.query_engine:
            return "[ERROR] Query engine not initialized"
        try:
            response = self.query_engine.query(question)
            return str(response)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"[ERROR] {type(e).__name__}"