# HotelMind AI – VisionRoot Day 15 Final Engineering Project

Python FastAPI hotel knowledge assistant with approved document ingestion (TXT/PDF/DOCX), small SQLite-backed vector retrieval, three safe tools, optional LLM answer generation, security controls and evaluation.

## Setup (VS Code terminal)

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows cmd:
# .venv\Scripts\activate.bat
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

Set admin key for uploads. For PowerShell:

```powershell
$env:HOTELMIND_ADMIN_KEY="replace-with-your-own-long-random-secret"
```

For cmd: `set HOTELMIND_ADMIN_KEY=replace-with-your-own-long-random-secret`.
Environment variables should be configured before starting the server. The `.env.example` file is a template only; this minimal project deliberately does not auto-load `.env`.

## Seed with fictional approved sample text

```bash
python -m scripts.seed_demo
```

## Run API

```bash
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try `GET /health`, `GET /documents`, `POST /chat`, `POST /tools/{tool_name}`, and `POST /documents/upload`.

Sample `POST /chat` request:

```json
{"question":"What time is check-in?"}
```

### Admin document upload

Upload only documents you are authorized to use, <=2 MB, extensions .txt/.pdf/.docx. Provide your `X-Admin-Key` as a request header. This is demonstration-only key protection, not a complete identity system.

### Optional real LLM

Set `OPENAI_API_KEY` in the terminal environment before starting the API and (optionally) `HOTELMIND_MODEL` to a model your account supports. The code calls the OpenAI Chat Completions API when configured. No key -> explicitly labeled `extractive-demo` excerpt. Keep credentials out of Git and screenshots.

## Evidence and tests

```bash
python -m pytest -v
python -m scripts.evaluate
```

The evaluation uses ten fixed questions against fictional hotel information and checks an expected phrase in the response. In `extractive-demo` mode this is a simple retrieval/excerpt evaluation, not a comprehensive measure of LLM answer quality.

## Safe tools

- `search_documents`: searches indexed knowledge.
- `get_hotel_policies`: searches policy-related information.
- `list_hotel_services`: searches services-related information.

All three are read-only. Other tool names return HTTP 403.

## Architecture

Read `docs/architecture.md` for diagram, components, limitations and what happens if components fail.

## Security limitations

Not production-ready without substantial security review (rate limiting, SSO, file scanning, robust secrets, prompt injection evaluation, logging, etc.). Use only fictional demo data for screenshots and evaluation.
