import json
from pathlib import Path
from app.config import ROOT
from app.orchestrator import answer

cases = json.loads((ROOT / 'tests' / 'evaluation_questions.json').read_text(encoding='utf-8'))
passed = 0
print('Question evaluation (literal expected phrase in answer):')
for i, case in enumerate(cases,1):
    result = answer(case['question'])
    ok = case['expected'].lower() in result['answer'].lower()
    passed += ok
    print(f"{i:02d} {'PASS' if ok else 'FAIL'} | {case['question']} | expected: {case['expected']} | source: {result['sources'][0]['filename'] if result['sources'] else 'none'}")
print(f'EVALUATION: {passed}/{len(cases)} passed')
