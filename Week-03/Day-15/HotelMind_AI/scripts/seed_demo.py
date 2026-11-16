from pathlib import Path
from app.ingestion import extract_text, chunk_text
from app.store import add_document
from app.config import ROOT

source = ROOT / 'data' / 'approved_documents' / 'demo_hotel.txt'
text = extract_text(source.name, source.read_bytes())
chunks = [line.strip() for line in text.splitlines() if line.strip()]  # one fact per chunk for this line-oriented demo file
id = add_document(source.name, chunks)
print(f'Indexed approved demo document id={id}, chunks={len(chunks)}')
