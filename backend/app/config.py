import os

from dotenv import load_dotenv

load_dotenv()


APP_NAME = "Arkiv API"
APP_VERSION = "2.0.0"

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

EMBED_MODEL = "models/gemini-embedding-001"
CHAT_MODEL = "gemini-2.5-flash-lite"

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

TOP_K = 5

MAX_FILE_SIZE = 50 * 1024 * 1024
ALLOWED_TYPES = {
    "pdf",
    "docx",
    "xlsx",
    "csv",
    "pptx",
    "txt",
    "md",
    "json",
    "png",
    "jpg",
    "jpeg",
}
UPLOAD_DIR = "data/uploads"

PROMPT = (
    "You are Arkiv, a helpful document assistant. "
    "Answer the question based ONLY on the provided context. "
    "If the context contains math or LaTeX, preserve them using $ for inline and $$ for display math. "
    "If you cannot answer from the context, say so honestly. "
    "Context: {context} Question: {question}"
)


# Manual
