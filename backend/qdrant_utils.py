from qdrant_client import QdrantClient, models
from config import QDRANT_HOST, COLLECTION_NAME

def initialize_qdrant(rebuild_if_exists: bool):
    host, port = QDRANT_HOST.split(":")
    client = QdrantClient(host=host, port=int(port))

    if rebuild_if_exists:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    collections = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE
            )
        )
    return client