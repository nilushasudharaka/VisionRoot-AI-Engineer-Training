import os
import glob
import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

DATA_FOLDER = "data"
CHROMA_FOLDER = "chroma_db"

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Create ChromaDB client
client = chromadb.PersistentClient(path=CHROMA_FOLDER)

# Create or get collection
collection = client.get_or_create_collection(
    name="company_knowledge"
)


def chunk_text(text, chunk_size=80, overlap=20):
    """
    Split text into small overlapping chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def ingest_documents():

    files = glob.glob(os.path.join(DATA_FOLDER, "*.txt"))

    if not files:
        print("No documents found.")
        return

    all_documents = []
    all_ids = []
    all_metadatas = []

    document_number = 1

    for file_path in files:

        filename = os.path.basename(file_path)

        print(f"\nProcessing: {filename}")

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        chunks = chunk_text(text)

        print(f"Created {len(chunks)} chunks")

        for chunk_number, chunk in enumerate(chunks):

            all_documents.append(chunk)

            all_ids.append(
                f"doc_{document_number}_chunk_{chunk_number}"
            )

            all_metadatas.append(
                {
                    "source": filename,
                    "chunk": chunk_number
                }
            )

        document_number += 1

    # Generate embeddings
    embeddings = embedding_model.encode(
        all_documents
    ).tolist()

    # Store in ChromaDB
    collection.upsert(
        ids=all_ids,
        documents=all_documents,
        embeddings=embeddings,
        metadatas=all_metadatas
    )

    print("\n===================================")
    print("DOCUMENT INGESTION COMPLETED")
    print("===================================")
    print(f"Documents processed: {len(files)}")
    print(f"Chunks stored: {len(all_documents)}")


if __name__ == "__main__":
    ingest_documents()