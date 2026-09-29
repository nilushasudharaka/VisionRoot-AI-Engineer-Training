documents = [
    {
        "id": "doc1",
        "text": """
        Retrieval-Augmented Generation, or RAG, combines document retrieval
        with a language model. The system first retrieves relevant information
        from a knowledge base and then provides that information to the LLM.
        RAG can reduce hallucinations when the retrieved information is relevant
        and accurate.
        """,
        "category": "RAG",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc2",
        "text": """
        Semantic search uses embeddings to understand the meaning of a query.
        Two sentences can have similar meanings even when they do not contain
        the same keywords. This makes semantic search useful for natural
        language questions.
        """,
        "category": "Retrieval",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc3",
        "text": """
        Keyword search looks for exact or closely matching words between the
        user's query and documents. It works especially well when the user
        searches for specific technical terms, product names, or identifiers.
        """,
        "category": "Retrieval",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc4",
        "text": """
        Hybrid search combines keyword search and semantic search. Keyword
        retrieval provides exact term matching while semantic retrieval
        provides meaning-based matching. Combining both methods can improve
        retrieval quality.
        """,
        "category": "Retrieval",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc5",
        "text": """
        Metadata filtering allows a retrieval system to restrict results based
        on information such as department, category, document type, date,
        author, or access level. Filtering can reduce irrelevant results.
        """,
        "category": "Retrieval",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc6",
        "text": """
        Top-K retrieval means selecting the K most relevant documents from the
        search results. A small K may miss useful information, while a large K
        may introduce irrelevant information into the LLM context.
        """,
        "category": "Retrieval",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc7",
        "text": """
        Reranking is a second-stage retrieval process. An initial retriever
        produces candidate documents, and a reranker examines the query and
        candidates more carefully to determine which documents are most
        relevant.
        """,
        "category": "Reranking",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc8",
        "text": """
        Retrieval quality is affected by document chunking, embedding models,
        search methods, metadata filters, similarity thresholds, and ranking
        strategies. Improving retrieval quality can improve the final RAG
        answer.
        """,
        "category": "Evaluation",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc9",
        "text": """
        A RAG system can produce an incorrect answer even when the language
        model is powerful. If the retriever returns irrelevant, incomplete,
        outdated, or misleading documents, the LLM may generate an answer
        based on incorrect context.
        """,
        "category": "RAG",
        "department": "AI",
        "year": 2026
    },

    {
        "id": "doc10",
        "text": """
        Excessive context can reduce answer quality. Providing too many
        retrieved documents may introduce unrelated information and make it
        harder for the language model to identify the important evidence.
        """,
        "category": "RAG",
        "department": "AI",
        "year": 2026
    }
]