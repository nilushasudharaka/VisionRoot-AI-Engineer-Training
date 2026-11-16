import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.getenv('HOTELMIND_DB_PATH', str(ROOT / 'data' / 'hotelmind.sqlite3')))
ADMIN_KEY = os.getenv('HOTELMIND_ADMIN_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
MODEL = os.getenv('HOTELMIND_MODEL', 'gpt-4.1-mini')
MAX_UPLOAD_BYTES = 2 * 1024 * 1024
MAX_QUESTION_LENGTH = 700
