import os

import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

from data.documents import documents


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

CHROMA_FOLDER = "chroma_db"
COLLECTION_NAME = "advanced_retrieval"

EMBEDDING_MODEL = "gemini-embedding-001"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ==========================================
# CHECK API KEY
# ==========================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# GEMINI EMBEDDING FUNCTION
# ==========================================

def create_embedding(text):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )

    return response.embeddings[0].values


# ==========================================
# CONNECT TO CHROMADB
# ==========================================

print("Connecting to ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)


# Delete old collection if it exists.
# This prevents dimension conflicts from previous tests.

try:
    chroma_client.delete_collection(
        name=COLLECTION_NAME
    )
except Exception:
    pass


collection = chroma_client.create_collection(
    name=COLLECTION_NAME
)


# ==========================================
# PREPARE DOCUMENTS
# ==========================================

ids = []
texts = []
metadatas = []
embeddings = []


print()
print("Creating Gemini embeddings...")


for index, document in enumerate(documents, start=1):

    print(
        f"Embedding document "
        f"{index}/{len(documents)}..."
    )

    ids.append(document["id"])

    texts.append(
        document["text"]
    )

    metadatas.append({
        "category": document["category"],
        "department": document["department"],
        "year": document["year"]
    })

    embedding = create_embedding(
        document["text"]
    )

    embeddings.append(embedding)


# ==========================================
# STORE DOCUMENTS
# ==========================================

collection.add(
    ids=ids,
    documents=texts,
    metadatas=metadatas,
    embeddings=embeddings
)


# ==========================================
# SUCCESS MESSAGE
# ==========================================

print()
print("=" * 60)
print("DOCUMENT INGESTION COMPLETED")
print("=" * 60)
print(
    f"Stored documents: {len(documents)}"
)
print(
    f"Collection: {COLLECTION_NAME}"
)
print(
    f"Embedding model: {EMBEDDING_MODEL}"
)
print("Embedding dimension: 768")
print("=" * 60)