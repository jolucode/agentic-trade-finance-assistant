import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "trade_finance"


class Retriever:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = self.client.get_collection(
            name=COLLECTION_NAME
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def search(self, query: str, top_k: int = 3):

        query_embedding = self.embedding_model.encode(
            [query]
        ).tolist()

        result = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=[
                "documents",
                "distances",
                "metadatas"
            ]
        )

        response = []

        for i in range(len(result["ids"][0])):
            response.append({
                "id": result["ids"][0][i],
                "text": result["documents"][0][i],
                "distance": result["distances"][0][i],
                "metadata": (
                    result["metadatas"][0][i]
                    if result["metadatas"]
                    else None
                )
            })

        return response