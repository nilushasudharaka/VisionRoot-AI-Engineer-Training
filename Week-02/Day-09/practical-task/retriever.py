import os
import re

import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder


# ==========================================
# CONFIGURATION
# ==========================================

CHROMA_FOLDER = "chroma_db"
COLLECTION_NAME = "advanced_retrieval"

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


# ==========================================
# LOAD MODELS
# ==========================================

print("Loading models...")

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
embedding_client = (
    genai.Client(api_key=GEMINI_API_KEY)
    if GEMINI_API_KEY
    else None
)

reranker = CrossEncoder(
    RERANKER_MODEL
)


# ==========================================
# CONNECT TO CHROMADB
# ==========================================

client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# ==========================================
# LOAD ALL DOCUMENTS
# ==========================================

all_data = collection.get(
    include=["documents", "metadatas"]
)

all_ids = all_data["ids"]
all_documents = all_data["documents"]
all_metadatas = all_data["metadatas"]


# ==========================================
# TOKENIZER
# ==========================================

def tokenize(text):

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )


# ==========================================
# BM25 KEYWORD SEARCH
# ==========================================

tokenized_documents = [
    tokenize(document)
    for document in all_documents
]

bm25 = BM25Okapi(
    tokenized_documents
)


def keyword_search(query, top_k=5):

    query_tokens = tokenize(query)

    scores = bm25.get_scores(
        query_tokens
    )

    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    results = []

    for index in ranked_indexes:

        results.append({
            "id": all_ids[index],
            "document": all_documents[index],
            "metadata": all_metadatas[index],
            "score": float(scores[index])
        })

    return results


# ==========================================
# SEMANTIC SEARCH
# ==========================================

def semantic_search(
    query,
    top_k=5,
    metadata_filter=None
):

    if embedding_client is None:
        raise ValueError(
            "GEMINI_API_KEY was not found in .env"
        )

    response = embedding_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    query_embedding = response.embeddings[0].values

    search_arguments = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if metadata_filter:
        search_arguments["where"] = metadata_filter

    results = collection.query(
        **search_arguments
    )

    output = []

    for i in range(len(results["ids"][0])):

        output.append({
            "id": results["ids"][0][i],
            "document": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": float(
                results["distances"][0][i]
            )
        })

    return output


# ==========================================
# HYBRID SEARCH
# ==========================================

def hybrid_search(
    query,
    top_k=5,
    metadata_filter=None
):

    keyword_results = keyword_search(
        query,
        top_k=top_k
    )

    semantic_results = semantic_search(
        query,
        top_k=top_k,
        metadata_filter=metadata_filter
    )

    combined = {}

    # Keyword results
    for result in keyword_results:

        combined[result["id"]] = {
            "id": result["id"],
            "document": result["document"],
            "metadata": result["metadata"],
            "keyword_score": result["score"],
            "semantic_score": 0.0
        }

    # Semantic results
    for result in semantic_results:

        if result["id"] not in combined:

            combined[result["id"]] = {
                "id": result["id"],
                "document": result["document"],
                "metadata": result["metadata"],
                "keyword_score": 0.0,
                "semantic_score": 0.0
            }

        # Convert distance into a simple similarity score.
        semantic_score = 1 / (
            1 + result["score"]
        )

        combined[result["id"]][
            "semantic_score"
        ] = semantic_score

    # Combine scores
    for result in combined.values():

        result["hybrid_score"] = (
            0.4 * result["keyword_score"]
            +
            0.6 * result["semantic_score"]
        )

    ranked_results = sorted(
        combined.values(),
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    return ranked_results[:top_k]


# ==========================================
# RERANKING
# ==========================================

def rerank(
    query,
    results,
    top_k=3
):

    if not results:
        return []

    pairs = [
        [query, result["document"]]
        for result in results
    ]

    scores = reranker.predict(
        pairs
    )

    for result, score in zip(
        results,
        scores
    ):

        result["rerank_score"] = float(score)

    reranked = sorted(
        results,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked[:top_k]