# Day 12 – AI Evaluation

**Program:** VisionRoot AI Engineer Trainee  
**Date:** 12 October 2026  
**Status:** In progress — 3 of 10 planned test cases reviewed

## Overview

This practical exercise introduces evaluation of AI-generated answers using the FastAPI AI application developed on Day 11. The goal is to compare expected and actual responses, identify issues such as unsupported claims, and document opportunities for improvement.

## Learning Objectives

- Understand accuracy, relevance, groundedness, faithfulness, hallucination, latency, and cost.
- Send test questions to an AI API and capture actual responses.
- Apply a consistent 0–2 scoring rubric and record observations.
- Recognize limitations when reference information is unavailable.
- Plan an improvement and assess it through repeat testing.

## Technologies

- Python 3
- FastAPI and Swagger UI (`/docs`) from the Day 11 application
- Python standard library (`csv`, `pathlib`)

## Proposed Folder Structure

```text
Week-03/
└── Day-12/
    ├── learning-notes.md
    └── practical-task/
        ├── evaluation.py
        ├── evaluation_results.csv   # created when the evaluation is saved
        └── README.md
```

> The structure above is the intended layout. Files not yet created should not be treated as completed deliverables.

## Evaluation Method

1. Start the existing Day 11 FastAPI application.
2. Open `http://127.0.0.1:8000/docs`.
3. Select the appropriate AI POST endpoint and submit a test question.
4. Copy the actual response (for example, the `data.response` value).
5. Compare the response with an expected answer supported by the test context.
6. Record scores and a brief explanation in the Day 12 evaluation workflow.

### Scoring Rubric

| Score | Meaning |
|---|---|
| 0 | Incorrect or fails the criterion |
| 1 | Partially meets the criterion |
| 2 | Meets the criterion |

**Metrics:** accuracy, relevance, groundedness, and faithfulness. Groundedness and faithfulness require an appropriate source or context for valid assessment. If no reference context exists, record the metric as **not verifiable** rather than treating a provisional score as confirmed.

## Tests Reviewed So Far

| # | Test Question | Observation |
|---|---|---|
| 1 | What is the check-in time? | The assistant requested more hotel information instead of giving a specific time. |
| 2 | What is the check-out time? | The assistant suggested 11:00 AM as a standard time, but no property-specific policy was available to verify it. |
| 3 | What is the price of a Deluxe room? | The assistant requested the property name rather than inventing a room price. |

**Progress:** 3 of 10 planned questions reviewed. The third test's suggested scores have not been confirmed as saved results. Some scores from the initial review were provisional because no hotel policy or pricing data was supplied.

## Running the Evaluation Script

From the `practical-task` folder, run:

```bash
python evaluation.py
```

When prompted, enter each actual response collected from the Day 11 API and the applicable scores and comments. If the script still contains all ten questions, completing only three does **not** produce a complete ten-question result set. Save completed records before exiting or update the script to support partial runs.

To start the Day 11 application, run the following command **from the directory containing its FastAPI `main.py`**, if that is its entry point:

```bash
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs`. Use the request format shown in Swagger UI for the available endpoint.

## Current Limitations

- The hotel questions were not backed by verified property-specific data.
- Groundedness and faithfulness scores could not be fully validated.
- Only three of ten test questions have been reviewed.
- Prompt improvement and before/after evaluation have not yet been completed.
- Measured API latency and usage cost have not yet been recorded.

## Next Steps

1. Replace or supplement hotel questions with test cases that match the AI application's actual capabilities and have verifiable expected answers.
2. Complete the remaining test cases and save the evaluation results.
3. Identify recurring failure modes from the results.
4. Make a documented prompt or application improvement.
5. Rerun the same questions, apply the same rubric, and compare baseline and improved results.
6. Update this README and `learning-notes.md` with verified findings.

## Conclusion

This Day 12 exercise introduced a practical workflow for assessing AI response quality. The initial three tests highlighted the importance of clear test context and verified reference data. The full evaluation and improvement comparison remain in progress.
