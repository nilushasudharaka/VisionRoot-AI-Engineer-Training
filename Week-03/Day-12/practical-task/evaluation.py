
import csv
import time
from pathlib import Path

QUESTIONS = [
    {
        "question": "What is the check-in time?",
        "expected": "The check-in time stated in the hotel policy."
    },
    {
        "question": "What is the check-out time?",
        "expected": "The check-out time stated in the hotel policy."
    },
    {
        "question": "What is the price of a Deluxe room?",
        "expected": "The Deluxe room price stated in the hotel data."
    },
    {
        "question": "Is breakfast included?",
        "expected": "The breakfast policy stated in the hotel data."
    },
    {
        "question": "Does the hotel provide free Wi-Fi?",
        "expected": "The Wi-Fi policy stated in the hotel data."
    },
    {
        "question": "Can I cancel my reservation?",
        "expected": "The cancellation policy stated in the hotel data."
    },
    {
        "question": "How many guests can stay in a Deluxe room?",
        "expected": "The guest capacity stated in the hotel data."
    },
    {
        "question": "Does the hotel provide airport transfers?",
        "expected": "The airport transfer policy stated in the hotel data."
    },
    {
        "question": "What facilities are available?",
        "expected": "The facilities listed in the hotel data."
    },
    {
        "question": "What is the price of a room not listed in the data?",
        "expected": "The AI should admit the information is unavailable."
    }
]

SCORES = [
    "accuracy",
    "relevance",
    "groundedness",
    "faithfulness"
]

def get_score(name):
    while True:
        try:
            score = int(input(f"{name} score (0, 1, or 2): "))
            if score in (0, 1, 2):
                return score
            print("Enter only 0, 1, or 2.")
        except ValueError:
            print("Please enter a number.")

def run_evaluation():
    results = []

    print("DAY 12 - AI EVALUATION")
    print("Test your AI using its actual responses.")
    print("Enter the response from your AI application.\n")

    for number, item in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {number}/10")
        print("Question:", item["question"])
        print("Expected:", item["expected"])

        actual = input("Paste actual AI answer: ").strip()

        start = time.perf_counter()
        # The AI response is entered above, so this measures
        # evaluation input time only, not AI response latency.
        elapsed = time.perf_counter() - start

        scores = {}
        for name in SCORES:
            scores[name] = get_score(name)

        comments = input("Comments / failure observed: ").strip()

        results.append({
            "question": item["question"],
            "expected_answer": item["expected"],
            "actual_answer": actual,
            **scores,
            "average_score": round(sum(scores.values()) / len(SCORES), 2),
            "latency_seconds": "",
            "cost": "",
            "comments": comments
        })

    output = Path("evaluation_results.csv")

    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    overall = sum(row["average_score"] for row in results) / len(results)
    percentage = overall / 2 * 100

    print("\n--- EVALUATION SUMMARY ---")
    print("Questions evaluated:", len(results))
    print(f"Average score: {overall:.2f}/2")
    print(f"Overall score: {percentage:.1f}%")
    print("Results saved to:", output.resolve())

if __name__ == "__main__":
    run_evaluation()
