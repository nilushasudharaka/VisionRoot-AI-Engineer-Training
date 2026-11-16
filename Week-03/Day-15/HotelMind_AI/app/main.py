from pathlib import Path
from fastapi import FastAPI, Header, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from . import config
from .security import require_admin, validate_question
from .ingestion import extract_text, chunk_text, EXTENSIONS
from .store import add_document, list_documents
from .orchestrator import answer, approved_tool

app = FastAPI(title='HotelMind AI – VisionRoot Day 15', version='1.0.0')

class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=700)

class ToolRequest(BaseModel):
    query: str = Field(min_length=1, max_length=700)

@app.get('/health')
def health():
    return {'status':'ok', 'mode': 'llm' if config.OPENAI_API_KEY else 'extractive-demo'}

@app.get('/documents')
def documents():
    return {'documents':list_documents()}

@app.post('/documents/upload')
async def upload_document(file: UploadFile = File(...), x_admin_key: str | None = Header(default=None)):
    require_admin(x_admin_key)
    filename = Path(file.filename or '').name
    if not filename or Path(filename).suffix.lower() not in EXTENSIONS:
        raise HTTPException(415, 'Only .pdf/.txt/.docx files are allowed')
    data = await file.read(config.MAX_UPLOAD_BYTES + 1)
    text = extract_text(filename, data)
    chunks = chunk_text(text)
    did = add_document(filename, chunks)
    return {'document_id': did, 'filename':filename, 'chunks':len(chunks), 'approved':True}

@app.post('/chat')
def chat(payload: QuestionRequest):
    return answer(payload.question)

@app.post('/tools/{tool_name}')
def invoke_tool(tool_name: str, payload: ToolRequest):
    # Safe approved tools are read-only; no filesystem, shell, or external actions.
    validate_question(payload.query)
    return {'tool':tool_name, 'results': approved_tool(tool_name, payload.query)}
