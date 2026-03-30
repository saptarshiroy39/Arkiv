import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Models
EMBED_MODEL = "models/gemini-embedding-001"
CHAT_MODEL = "gemini-2.5-flash-lite"

# Chunking
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200

# RAG
TOP_K = 5

# Limits
MAX_FILE_SIZE = 50 * 1024 * 1024
ALLOWED_TYPES = {"pdf", "docx", "xlsx", "csv", "pptx", "txt", "md", "json"}
