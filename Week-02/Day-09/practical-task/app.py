import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

from retriever import (
    keyword_search,
    semantic_search,
    hybrid_search,
    rerank
)


# ==========================================
# ENVIRONMENT
# ==========================================

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


# ==========================================
# GEMINI CLIENT
# ==========================================

if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY was not found in .env"
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

def display_results(
    title,
    results
):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    if not results:

        print("No results found.")

        return

    for index, result in enumerate(
        results,
        start=1
    ):

        print()
        print(
            f"{index}. ID: {result['id']}"
        )

        print(
            f"Category: "
            f"{result['metadata'].get('category')}"
        )

        print(
            f"Document: "
            f"{result['document'].strip()}"
        )

        if "keyword_score" in result:

            print(
                f"Keyword Score: "
                f"{result['keyword_score']:.4f}"
            )

        if "semantic_score" in result:

            print(
                f"Semantic Score: "
                f"{result['semantic_score']:.4f}"
            )

        if "hybrid_score" in result:

            print(
                f"Hybrid Score: "
                f"{result['hybrid_score']:.4f}"
            )

        if "rerank_score" in result:

            print(
                f"Rerank Score: "
                f"{result['rerank_score']:.4f}"
            )


# ==========================================
# GEMINI ANSWER
# ==========================================

def generate_answer(
    question,
    results
):

    context = "\n\n".join(
        [
            result["document"]
            for result in results
        ]
    )

    prompt = f"""
You are a helpful RAG assistant.

Answer the user's question using only
the provided context.

If the answer is not available in the
context, clearly say that the information
was not found.

Do not invent information.

Context:
{context}

Question:
{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except ServerError:

        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt
        )

        return response.text


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    print("=" * 70)
    print("ADVANCED RETRIEVAL RAG SYSTEM")
    print("=" * 70)

    print()
    print("Enter your question.")
    print("Type 'exit' to stop.")

    while True:

        question = input(
            "\nQuestion: "
        ).strip()

        if question.lower() == "exit":

            print(
                "Application closed."
            )

            break

        if not question:

            print(
                "Please enter a question."
            )

            continue

        # ----------------------------------
        # 1. Keyword Search
        # ----------------------------------

        keyword_results = keyword_search(
            question,
            top_k=5
        )

        display_results(
            "KEYWORD SEARCH RESULTS",
            keyword_results
        )

        # ----------------------------------
        # 2. Semantic Search
        # ----------------------------------

        semantic_results = semantic_search(
            question,
            top_k=5
        )

        display_results(
            "SEMANTIC SEARCH RESULTS",
            semantic_results
        )

        # ----------------------------------
        # 3. Hybrid Search
        # ----------------------------------

        hybrid_results = hybrid_search(
            question,
            top_k=5
        )

        display_results(
            "HYBRID SEARCH RESULTS",
            hybrid_results
        )

        # ----------------------------------
        # 4. Reranking
        # ----------------------------------

        reranked_results = rerank(
            question,
            hybrid_results,
            top_k=3
        )

        display_results(
            "RERANKED RESULTS",
            reranked_results
        )

        # ----------------------------------
        # 5. Gemini
        # ----------------------------------

        answer = generate_answer(
            question,
            reranked_results
        )

        print()
        print("=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)

        print(answer)


if __name__ == "__main__":
    main()