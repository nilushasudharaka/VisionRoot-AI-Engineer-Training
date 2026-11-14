import unittest
from optimizer import OptimizedAssistant, estimate_tokens, retrieve, select_model, validate_answer


class TestOptimization(unittest.TestCase):
    def test_retrieval_matches(self):
        self.assertIn("Wi-Fi", retrieve("Is Wi-Fi available?")[0])

    def test_retrieval_top_k(self):
        self.assertLessEqual(len(retrieve("check-in pool airport", top_k=2)), 2)

    def test_unrelated_question_abstains(self):
        self.assertEqual(retrieve("Can I bring a pet?"), [])

    def test_model_selection_simple(self):
        self.assertEqual(select_model("Is Wi-Fi available?"), "small-demo")

    def test_model_selection_complex(self):
        self.assertEqual(select_model("Compare hotel policies"), "large-demo")

    def test_cache_avoids_model_call(self):
        assistant = OptimizedAssistant()
        assistant.ask("What time is check-in?")
        hit = assistant.ask("  WHAT time is check-in?  ")
        self.assertTrue(hit.cache_hit)
        self.assertEqual(assistant.model_calls, 1)
        self.assertEqual(hit.model_calls, 0)

    def test_cache_avoids_cost(self):
        assistant = OptimizedAssistant()
        assistant.ask("What time is check-in?")
        self.assertEqual(assistant.ask("What time is check-in?").estimated_cost_usd, 0)

    def test_context_limited(self):
        result = OptimizedAssistant().ask("What time is check-in?")
        self.assertLessEqual(result.retrieved_documents, 2)

    def test_quality_check(self):
        self.assertTrue(validate_answer("Grounded answer", ["Grounded answer"]))
        self.assertFalse(validate_answer("Unsourced answer", ["Grounded answer"]))

    def test_token_estimate(self):
        self.assertGreater(estimate_tokens("some example text"), 0)

    def test_metrics_available(self):
        result = OptimizedAssistant().ask("Is Wi-Fi available?")
        self.assertGreaterEqual(result.retrieval_ms, 0)
        self.assertGreaterEqual(result.model_ms, 0)
        self.assertGreaterEqual(result.processing_ms, 0)
        self.assertGreaterEqual(result.total_ms, 0)

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            OptimizedAssistant().ask("   ")

    def test_answer_grounded(self):
        result = OptimizedAssistant().ask("What time is check-in?")
        self.assertTrue(result.quality_pass)


if __name__ == "__main__":
    unittest.main(verbosity=2)
