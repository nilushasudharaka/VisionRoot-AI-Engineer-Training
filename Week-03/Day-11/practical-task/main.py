import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from google import genai


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_KEY = os.getenv("API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="VisionRoot AI API",
    description="Production-style AI API built with FastAPI",
    version="1.0.0"
)


# ==========================================
# REQUEST MODELS
# ==========================================

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Message to send to the AI"
    )


class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Text to summarize"
    )


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Question to ask the AI"
    )


# ==========================================
# RESPONSE HELPER
# ==========================================

def success_response(data):
    return {
        "success": True,
        "data": data,
        "error": None
    }


# ==========================================
# AUTHENTICATION
# ==========================================

def verify_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def root():
    return {
        "message": "VisionRoot AI API is running",
        "status": "healthy"
    }


# ==========================================
# CHAT ENDPOINT
# ==========================================

@app.post("/api/ai/chat")
def chat(
    request: ChatRequest,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    logger.info("Chat request received")

    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=request.message
        )

        return success_response({
            "response": response.text
        })

    except Exception as e:
        logger.error("Chat request failed: %s", str(e))

        raise HTTPException(
            status_code=500,
            detail="AI service temporarily unavailable"
        )


# ==========================================
# SUMMARIZE ENDPOINT
# ==========================================

@app.post("/api/ai/summarize")
def summarize(
    request: SummarizeRequest,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    logger.info("Summarization request received")

    prompt = f"""
Summarize the following text clearly and briefly.

Text:
{request.text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return success_response({
            "summary": response.text
        })

    except Exception as e:
        logger.error("Summarization failed: %s", str(e))

        raise HTTPException(
            status_code=500,
            detail="AI service temporarily unavailable"
        )


# ==========================================
# ASK ENDPOINT
# ==========================================

@app.post("/api/ai/ask")
def ask(
    request: AskRequest,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    logger.info("Question request received")

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=request.question
        )

        return success_response({
            "answer": response.text
        })

    except Exception as e:
        logger.error("Question request failed: %s", str(e))

        raise HTTPException(
            status_code=500,
            detail="AI service temporarily unavailable"
        )