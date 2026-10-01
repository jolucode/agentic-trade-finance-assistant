from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


DATA_PATH = Path("data/trade_finance_guide.txt")

COLLECTION_NAME = "trade_finance"

CHROMA_PATH = "chroma_db"


def load_document() -> str:
    return DATA_PATH.read_text(
        encoding="utf-8"
    )


def split_document(text: str) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    return splitter.split_text(text)


def create_embeddings(chunks: list[str]) -> list[list[float]]:

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    embeddings = model.encode(chunks)

    return embeddings.tolist()


def save_to_vector_db(
    chunks: list[str],
    embeddings: list[list[float]]
):

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    ids = [
        f"chunk-{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )


def ingest():

    print("Loading document...")

    text = load_document()

    print("Splitting document...")

    chunks = split_document(text)

    print(
        f"Chunks created: {len(chunks)}"
    )

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Saving to vector database...")

    save_to_vector_db(
        chunks,
        embeddings
    )

    print("Ingestion completed.")


if __name__ == "__main__":
    ingest()