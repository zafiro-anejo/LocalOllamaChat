from pathlib import Path
from tqdm import tqdm
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Document as LlamaDocument,
)
from llama_index.core.node_parser import SimpleNodeParser
from chunking import build_dynamic_chunks

def build_index(storage_context: StorageContext, source_dir: Path):
    all_nodes = []
    md_files = list(source_dir.glob("*.md"))

    if not md_files:
        raise FileNotFoundError(f"[ERROR] No .md files in {source_dir}")

    for md_file in tqdm(md_files, desc="Processing documents"):
        with open(md_file, "r", encoding="utf-8") as f:
            document_text = f.read()

        final_chunks = build_dynamic_chunks(document_text)
        documents = [LlamaDocument(text=chunk) for chunk in final_chunks]
        parser = SimpleNodeParser.from_defaults()
        nodes = parser.get_nodes_from_documents(documents)
        all_nodes.extend(nodes)

    storage_context.docstore.add_documents(all_nodes)

    index = VectorStoreIndex(
        all_nodes,
        storage_context=storage_context,
        show_progress=True
    )
    return index