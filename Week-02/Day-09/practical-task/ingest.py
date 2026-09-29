import os

import chromadb
from sentence_transformers import SentenceTransformer

from data.documents import documents


# ==========================================
# CONFIGURATION
# ==========================================

CHROMA_FOLDER = "chroma_db"
COLLECTION_NAME = "advanced_retrieval"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

model = SentenceTransformer(EMBEDDING_MODEL)


# ==========================================
# CONNECT TO CHROMADB
# ==========================================

client = chromadb.PersistentClient(path=CHROMA_FOLDER)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# ==========================================
# PREPARE DATA
# ==========================================

ids = []
texts = []
metadatas = []
embeddings = []


for document in documents:

    ids.append(document["id"])

    texts.append(document["text"])

    metadatas.append({
        "category": document["category"],
        "department": document["department"],
        "year": document["year"]
    })

    embedding = model.encode(document["text"]).tolist()

    embeddings.append(embedding)


# ==========================================
# STORE DOCUMENTS
# ==========================================

collection.upsert(
    ids=ids,
    documents=texts,
    metadatas=metadatas,
    embeddings=embeddings
)


print()
print("==========================================")
print("DOCUMENT INGESTION COMPLETED")
print("==========================================")
print(f"Stored documents: {len(documents)}")
print(f"Collection: {COLLECTION_NAME}")
print("==========================================")