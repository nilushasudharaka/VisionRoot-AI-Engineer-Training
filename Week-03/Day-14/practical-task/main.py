from optimizer import OptimizedAssistant, DOCUMENTS, estimate_tokens

assistant = OptimizedAssistant()
questions = [
    "What time is check-in?",
    "What time is check-in?",  # identical question should avoid second model call
    "Is Wi-Fi available?",
    "How can I request airport transfers?",
    "What is the cancellation policy?",
    "Can I bring a pet?",  # should abstain when no matching document is available
]

print("VISIONROOT DAY 14 – AI OPTIMIZATION DEMO")
print("Note: MODEL CALLS ARE SIMULATED; token counts and prices are illustrative.\n")
for question in questions:
    result = assistant.ask(question)
    print(f"Q: {question}\nA: {result.answer}")
    print(f"  model={result.model}, cache_hit={result.cache_hit}, model_calls={result.model_calls}")
    print(f"  retrieved={result.retrieved_documents}, estimated_input_tokens={result.estimated_input_tokens}, "
          f"estimated_output_tokens={result.estimated_output_tokens}")
    print(f"  estimated_cost=${result.estimated_cost_usd:.8f}, "
          f"retrieval={result.retrieval_ms:.4f}ms, model={result.model_ms:.4f}ms, "
          f"processing={result.processing_ms:.4f}ms, total={result.total_ms:.4f}ms")
    print(f"  quality_check={'PASS' if result.quality_pass else 'FAIL'}\n")

baseline = sum(estimate_tokens("Question: " + q + "\nContext:\n" + "\n".join(DOCUMENTS)) for q in questions)
actual = sum(assistant.cache[q.casefold()].estimated_input_tokens for q in dict.fromkeys(questions))
print("SUMMARY")
print(f"Requests: {len(questions)}")
print(f"Simulated model calls: {assistant.model_calls}")
print(f"Calls avoided by exact-match caching: {len(questions) - assistant.model_calls}")
print(f"Naive full-context estimated input tokens across requests: {baseline}")
print(f"Optimized estimated input tokens across non-cached requests: {actual}")
print("These metrics do not measure real API latency, cost, or model quality.")
