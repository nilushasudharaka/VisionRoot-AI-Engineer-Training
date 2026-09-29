# Day 9 - Advanced Retrieval Test Results

## Test 1 - Hybrid Search

Question:

What is hybrid search?

### Keyword Search

Record the top results here.

### Semantic Search

Record the top results here.

### Hybrid Search

Record the top results here.

### Reranked Results

Record the top results here.

### Observation

Hybrid search combined exact keyword matching with
semantic similarity. Reranking changed the order of
some candidate documents based on query-document
relevance.

---

## Test 2 - Semantic Search

Question:

How can a system understand the meaning of a question
instead of only matching exact words?

### Observation

Semantic search was useful because the query did not
necessarily contain the exact terminology used in the
document.

---

## Test 3 - Metadata Filtering

Question:

How can retrieval results be restricted to a specific
category?

Filter:

category = Retrieval

### Observation

Metadata filtering restricted the search results to
documents belonging to the selected category.

---

## Test 4 - Top-K Comparison

Question:

What is RAG?

### Top-K = 3

Record observations here.

### Top-K = 5

Record observations here.

### Top-K = 10

Record observations here.

### Observation

Increasing Top-K provides more candidate information,
but excessive context can introduce irrelevant
information.

---

# Retrieval Quality Investigation

## Why can RAG provide a wrong answer even when the LLM is strong?

A strong LLM can still produce an incorrect RAG answer
when the retrieved context is incorrect, incomplete,
irrelevant, outdated, or poorly ranked.

Possible causes include:

1. Poor document chunking
2. Incorrect retrieval
3. Weak embeddings
4. Incorrect metadata filtering
5. Poor Top-K selection
6. Poor reranking
7. Missing information
8. Excessive context
9. Prompt problems
10. Hallucination by the LLM