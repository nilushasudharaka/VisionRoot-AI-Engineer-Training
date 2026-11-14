"""VisionRoot Day 14: measurable, local AI optimization demo.

No actual LLM API is called. Rates, token counts, and model outputs are demonstrations.
"""
from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
import re

DOCUMENTS = [
    "Hotel check-in starts at 2 PM and check-out is before 11 AM.",
    "Free Wi-Fi is available in guest rooms and common areas.",
    "Airport transfers can be requested at reception for an additional fee.",
    "The swimming pool opens at 7 AM and closes at 8 PM.",
    "Reservations may be cancelled without a fee up to 48 hours before arrival.",
]
STOP_WORDS = {"the", "a", "an", "is", "are", "at", "in", "on", "of", "to", "for", "what", "when", "does", "do", "can", "i", "you", "your", "and", "how", "hotel", "about"}
# Illustrative prices only; not provider pricing (USD per 1 million tokens).
DEMO_PRICES = {"small-demo": (0.20, 0.80), "large-demo": (2.00, 8.00)}


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP_WORDS}


def estimate_tokens(text: str) -> int:
    """Rough local approximation, NOT provider-reported tokens."""
    return max(1, (len(text) + 3) // 4) if text else 0


def retrieve(question: str, documents=DOCUMENTS, top_k=2) -> list[str]:
    """Keyword-overlap ranking, limited to top_k documents with positive matches."""
    query = tokens(question)
    scored = [(len(query & tokens(doc)), i, doc) for i, doc in enumerate(documents)]
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [doc for score, _, doc in scored if score > 0][:top_k]


def select_model(question: str) -> str:
    """Simple demonstrative rule, not a production capability evaluator."""
    complex_terms = {"compare", "analyze", "analyse", "explain", "evaluate", "why", "tradeoff"}
    return "large-demo" if tokens(question) & complex_terms else "small-demo"


def simulated_model(question: str, context: list[str]) -> str:
    """Deterministic stand-in for an LLM, intentionally no network calls."""
    if not context:
        return "I don't have enough information in the provided documents."
    # Show grounded reference snippet, not generated factual reasoning.
    return context[0]


def validate_answer(answer: str, context: list[str]) -> bool:
    """Baseline quality check; permits abstention, requires sourced snippet otherwise."""
    return answer == "I don't have enough information in the provided documents." or answer in context


@dataclass
class Result:
    answer: str
    model: str
    cache_hit: bool
    retrieved_documents: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_cost_usd: float
    retrieval_ms: float
    model_ms: float
    processing_ms: float
    total_ms: float
    quality_pass: bool
    model_calls: int


class OptimizedAssistant:
    def __init__(self, docs=None):
        self.docs = list(DOCUMENTS if docs is None else docs)
        self.cache: dict[str, Result] = {}
        self.model_calls = 0

    def ask(self, question: str) -> Result:
        start = perf_counter()
        clean = " ".join(question.strip().split())
        if not clean:
            raise ValueError("Question cannot be empty")
        key = clean.casefold()
        if key in self.cache:
            old = self.cache[key]
            return Result(old.answer, old.model, True, old.retrieved_documents,
                          0, 0, 0.0, 0.0, 0.0,
                          (perf_counter()-start)*1000,
                          (perf_counter()-start)*1000, old.quality_pass, 0)

        t_retrieve = perf_counter()
        context = retrieve(clean, self.docs, top_k=2)
        retrieval_ms = (perf_counter() - t_retrieve) * 1000

        model = select_model(clean)
        # Context deliberately restricted to ranked matches instead of all documents.
        prompt = f"Question: {clean}\nContext:\n" + "\n".join(context)
        input_count = estimate_tokens(prompt)
        t_model = perf_counter()
        answer = simulated_model(clean, context)
        model_ms = (perf_counter() - t_model) * 1000
        self.model_calls += 1
        output_count = estimate_tokens(answer)
        in_price, out_price = DEMO_PRICES[model]
        cost = (input_count * in_price + output_count * out_price) / 1_000_000

        t_process = perf_counter()
        quality_pass = validate_answer(answer, context)
        processing_ms = (perf_counter() - t_process) * 1000
        total_ms = (perf_counter() - start) * 1000
        result = Result(answer, model, False, len(context), input_count,
                        output_count, cost, retrieval_ms, model_ms,
                        processing_ms, total_ms, quality_pass, 1)
        self.cache[key] = result
        return result
