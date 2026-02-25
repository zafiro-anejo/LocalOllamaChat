import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

INITIAL_FILES_DIR = BASE_DIR / "initial_files"
PROCESSED_FILES_DIR = BASE_DIR / "processed_files"

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost:6333")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

EMBED_MODEL = "bge-m3"
LLM_MODEL = "gemma3"
CHUNKING_LLM_MODEL = "gemma3"
VLM_MODEL = "qwen3-vl:2b"

VLM_API_PARAMS = {"think": False, "seed": 42, "max_completion_tokens": 256}
VLM_TIMEOUT = 90

PAGE_BREAK_PLACEHOLDER = "<!-- page_break -->"
IMAGE_DESCRIPTION_START = "<image_description>"
IMAGE_DESCRIPTION_END = "</image_description>"

COLLECTION_NAME = "yandex"
SIMILARITY_TOP_K = 5
HYBRID_TOP_K = 10
RERANK_TOP_N = 5

CHUNKING_SPLIT_PATTERN = "\n#"
MIN_CHUNK_WORDS = 200
MAX_CHUNK_WORDS = 1000

DOCLING_DO_OCR = False
DOCLING_DO_TABLE_STRUCTURE = True
DOCLING_GENERATE_PICTURE_IMAGES = True
DOCLING_DO_PICTURE_DESCRIPTION = True
TABLE_STRUCTURE_MODE = "accurate"