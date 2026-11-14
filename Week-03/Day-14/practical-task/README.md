# VisionRoot — Day 14: AI Optimization

## Objective
Demonstrate techniques for reducing unnecessary LLM calls, model selection, caching, retrieval ranking, context reduction, cost estimation, answer checks, and latency breakdowns.

## Run (Python 3.9+; no extra packages)

```bash
python main.py
python -m unittest test_optimizer.py -v
```

## Techniques
- **Fewer calls:** exact-match response cache prevents duplicate simulated model calls.
- **Model selection:** rule-based routing to `small-demo` and `large-demo`.
- **Cache:** in-memory response cache; clears on process exit.
- **Retrieval:** overlap ranking over five example hotel-policy snippets; top 2 only.
- **Context:** only relevant snippets sent to simulated model, not all documents.
- **Cost:** estimated character-based token counts and illustrative USD token rates.
- **Quality:** answer must be a retrieved snippet or the fallback abstention.
- **Latency:** `perf_counter()` timing around local retrieval, simulated model, validation, and total processing.

## Limitations
- No real LLM API request is made. Local latency is **not representative of remote API latency**.
- Rates are **made-up examples**, not vendor quotes; token counting is approximate.
- Keyword overlap is not semantic retrieval; small test corpus uses whole lines instead of genuine chunking.
- Model-selection rules do not measure actual model capabilities.
- The quality check only detects whether output is a snippet; it cannot prove factual correctness.
- Exact-match cache does not support similar paraphrased queries and is not persistent.
- Use real provider usage telemetry, pricing, a held-out quality set, and API timings for production.

## Evidence for daily submission
Run the demo and unit tests and take screenshots. Add the actual Git commit hash after committing.
