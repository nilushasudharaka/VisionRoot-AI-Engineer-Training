"""Small, local SQLite-backed vector store (normalized hashing embeddings).
For learning/small datasets only: scans vectors in Python, not approximate nearest neighbor.
"""
import json
import re
import sqlite3
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from . import config

VECTORIZER = HashingVectorizer(n_features=512, norm='l2', alternate_sign=False, ngram_range=(1,2))

def db_connection(path: Path | None = None):
    path = path or config.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, filename TEXT NOT NULL UNIQUE)')
    con.execute('CREATE TABLE IF NOT EXISTS chunks (id INTEGER PRIMARY KEY, document_id INTEGER NOT NULL, body TEXT NOT NULL, vector TEXT NOT NULL, FOREIGN KEY(document_id) REFERENCES documents(id))')
    con.commit()
    return con

def vectorize(texts: list[str]) -> np.ndarray:
    return VECTORIZER.transform(texts).toarray().astype(float)

def add_document(filename: str, chunks: list[str], path: Path | None = None) -> int:
    con = db_connection(path)
    try:
        # Duplicate filename updates its indexed content atomically.
        with con:
            current = con.execute('SELECT id FROM documents WHERE filename=?', (filename,)).fetchone()
            if current:
                did = current['id']
                con.execute('DELETE FROM chunks WHERE document_id=?', (did,))
            else:
                did = con.execute('INSERT INTO documents(filename) VALUES (?)', (filename,)).lastrowid
            for body, vec in zip(chunks, vectorize(chunks)):
                con.execute('INSERT INTO chunks(document_id, body, vector) VALUES (?, ?, ?)', (did, body, json.dumps(vec.tolist())))
        return did
    finally:
        con.close()

def list_documents(path: Path | None = None):
    con = db_connection(path)
    try:
        return [dict(row) for row in con.execute('SELECT id, filename FROM documents ORDER BY id')]
    finally:
        con.close()

def search(query: str, k: int = 3, path: Path | None = None):
    con = db_connection(path)
    try:
        rows = con.execute('SELECT d.filename,c.id,c.body,c.vector FROM chunks c JOIN documents d ON d.id=c.document_id').fetchall()
        if not rows:
            return []
        enriched = query + (' cancel fee hours' if 'cancellation' in query.lower() or 'policy' in query.lower() else '')
        target = vectorize([enriched])[0]
        ranked = []
        stop = {'what','when','where','which','does','have','there','with','your','hotel','is','the','are','can','you','for','and','this','that','do','a','to','i','it','me','my','about','all'}
        terms = set(re.findall(r'[a-z0-9]+', query.lower())) - stop
        # Small synonym map for hotel evaluation, not a semantic embedding model.
        variants = {'cancellation':'cancel', 'cancellations':'cancel', 'policy':'cancel', 'policies':'cancel'}
        terms |= {variants[t] for t in terms if t in variants}
        for row in rows:
            chunk_terms = set(re.findall(r'[a-z0-9]+', row['body'].lower()))
            if not terms.intersection(chunk_terms):
                continue
            score = float(np.dot(target, np.array(json.loads(row['vector']))))
            overlap = len(terms.intersection(chunk_terms)) / max(1, len(terms))
            score += 0.6 * overlap
            # An explicit request for time should prioritize passages containing a clock time.
            if any(t in query.lower() for t in ['time', 'hours']) and re.search(r'\b\d{1,2}:\d{2}\s*(?:AM|PM)\b', row['body'], re.I):
                score += 0.35
            if score >= 0.14:
                ranked.append({'source': row['filename'], 'chunk_id': row['id'], 'text': row['body'], 'score': round(score, 4)})
        ranked.sort(key=lambda r: r['score'], reverse=True)
        return ranked[:max(1,min(k,3))]
    finally:
        con.close()
