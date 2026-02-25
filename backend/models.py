from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from config import EMBED_MODEL, LLM_MODEL, OLLAMA_BASE_URL

def setup_models():
    Settings.embed_model = OllamaEmbedding(
        model_name=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
        ollama_additional_kwargs={"mirostat": 0}
    )
    Settings.llm = Ollama(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1,
        timeout=300.0,
        request_timeout=300.0,
        keep_alive=300.0
    )