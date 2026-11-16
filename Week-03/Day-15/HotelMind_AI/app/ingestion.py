from io import BytesIO
from pathlib import Path
import re
from fastapi import HTTPException
from pypdf import PdfReader
from docx import Document
from .config import MAX_UPLOAD_BYTES

EXTENSIONS = {'.txt', '.pdf', '.docx'}

def extract_text(filename: str, data: bytes) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in EXTENSIONS:
        raise HTTPException(415, 'Only approved .txt, .pdf, .docx uploads supported')
    if not data or len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, 'Document empty or exceeds 2 MB limit')
    try:
        if extension == '.txt':
            text = data.decode('utf-8')
        elif extension == '.pdf':
            reader = PdfReader(BytesIO(data))
            if reader.is_encrypted or len(reader.pages) > 30:
                raise ValueError('Encrypted or excessively long PDF')
            text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        else:
            document = Document(BytesIO(data))
            text = '\n'.join(p.text for p in document.paragraphs)
            for table in document.tables:
                text += '\n' + '\n'.join(' | '.join(c.text for c in row.cells) for row in table.rows)
    except (ValueError, UnicodeError, KeyError, TypeError, Exception) as exc:
        raise HTTPException(422, 'Could not extract document text') from exc
    text = re.sub(r'\r\n?', '\n', text)
    if not text.strip():
        raise HTTPException(422, 'Document contains no extractable text (scanned PDFs need OCR)')
    return text.strip()

def chunk_text(text: str, limit: int = 650) -> list[str]:
    """Group short lines while capping long paragraphs; small baseline chunker."""
    chunks, acc = [], ''
    paragraphs = [p.strip() for p in re.split(r'\n+', text) if p.strip()]
    for para in paragraphs:
        words = para.split()
        segments, segment = [], ''
        for word in words:
            if len(segment) + len(word) + 1 > limit and segment:
                segments.append(segment); segment = ''
            segment = (segment + ' ' + word).strip()
        if segment:
            segments.append(segment)
        for piece in segments:
            if acc and len(acc) + len(piece) + 1 > limit:
                chunks.append(acc); acc = ''
            acc = (acc + '\n' + piece).strip()
    if acc:
        chunks.append(acc)
    return chunks
