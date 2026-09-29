from retriever import semantic_search


print("=" * 60)
print("METADATA FILTERING TEST")
print("=" * 60)


# Search only documents where:
# category = Retrieval

results = semantic_search(
    query="How does retrieval work?",
    top_k=5,
    metadata_filter={
        "category": "RAG"
    }
)


print()
print("Results:")
print()


for number, result in enumerate(results, start=1):

    print(f"Result {number}")
    print(f"ID: {result['id']}")
    print(f"Category: {result['metadata']['category']}")
    print(f"Department: {result['metadata']['department']}")
    print(f"Year: {result['metadata']['year']}")
    print(f"Document: {result['document'].strip()}")
    print("-" * 60)
    