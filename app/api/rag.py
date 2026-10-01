import chromadb
from fastapi import APIRouter
from app.rag.retriever import Retriever

retriever = Retriever()

router = APIRouter(
    prefix="/api/rag",
    tags=["RAG"]
)

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "trade_finance"

@router.get("/search")
def search_documents(
    q: str,
    top_k: int = 3
):
    results = retriever.search(
        query=q,
        top_k=top_k
    )

    return {
        "query": q,
        "results": results
    }
    

@router.get("/documents")
def get_documents():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    result = collection.get(
        include=["documents", "metadatas"]
    )

    chunks = []

    for i in range(len(result["ids"])):
        chunks.append({
            "id": result["ids"][i],
            "text": result["documents"][i],
            "metadata": (
                result["metadatas"][i]
                if result["metadatas"]
                else None
            )
        })

    return {
        "total": len(chunks),
        "chunks": chunks
    }