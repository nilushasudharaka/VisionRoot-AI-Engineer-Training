import re
import secrets
from fastapi import HTTPException
from . import config

PATTERNS = [r'ignore (all )?(previous|prior) instructions', r'reveal (your )?(system prompt|hidden instructions)', r'act as if you have no restrictions', r'ignore your (safety )?rules']
SENSITIVE = [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', r'\bsk-[A-Za-z0-9_-]{10,}\b', r'\b(?:\d[ -]?){13,19}\b']

def validate_question(q: str) -> str:
    if not isinstance(q, str) or not q.strip() or len(q) > config.MAX_QUESTION_LENGTH:
        raise HTTPException(status_code=422, detail='Question must be 1 to 700 characters.')
    if any(re.search(p, q, re.I) for p in PATTERNS):
        raise HTTPException(status_code=400, detail='Known prompt-injection phrase rejected.')
    return q.strip()

def redact(text: str) -> str:
    for pattern in SENSITIVE:
        text = re.sub(pattern, '[REDACTED]', text, flags=re.I)
    return text

def require_admin(key: str | None) -> None:
    if not config.ADMIN_KEY or not key or not secrets.compare_digest(key, config.ADMIN_KEY):
        raise HTTPException(status_code=401, detail='Valid X-Admin-Key required. Set HOTELMIND_ADMIN_KEY.')

ALLOWED_TOOLS = {'search_documents', 'get_hotel_policies', 'list_hotel_services'}

def verify_tool(name: str) -> str:
    if name not in ALLOWED_TOOLS:
        raise HTTPException(status_code=403, detail='Tool not approved.')
    return name
