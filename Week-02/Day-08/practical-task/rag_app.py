import os

import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai


load_dotenv()


# ==========================================
# CONFIGURATION
# ==========================================

CHROMA_FOLDER = "chroma_db"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


# ==========================================
# INITIALIZE MODELS AND DATABASE
# ==========================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)

collection = client.get_collection(
    name="company_knowledge"
)

gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# RETRIEVAL
# ==========================================

def retrieve_documents(question, top_k=3):

    question_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    return documents, metadatas


# ==========================================
# GENERATION
# ==========================================

def generate_answer(question, documents, metadatas):

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        source = metadata["source"]
        chunk = metadata["chunk"]

        context_parts.append(
            f"Source: {source}\n"
            f"Chunk: {chunk}\n"
            f"Content: {document}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a Company Knowledge Assistant.

Answer the user's question using ONLY the
information provided in the context.

If the answer is not available in the context,
say:

"I could not find this information in the
available company documents."

Do not invent information.

Include the source filename(s) used for the answer.

CONTEXT:
{context}

USER QUESTION:
{question}

Provide:
1. Answer
2. Sources
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    print("=" * 60)
    print("COMPANY KNOWLEDGE ASSISTANT")
    print("=" * 60)

    print("\nAsk questions about the available documents.")
    print("Type 'exit' to close the application.")

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question.strip():
            print("Please enter a question.")
            continue

        print("\nSearching knowledge base...")

        documents, metadatas = retrieve_documents(
            question,
            top_k=3
        )

        print("\nGenerating answer...")

        answer = generate_answer(
            question,
            documents,
            metadatas
        )

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)

        print(answer)


if __name__ == "__main__":
    main()