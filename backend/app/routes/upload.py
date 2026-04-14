import os

from app.config import ALLOWED_TYPES, MAX_FILE_SIZE, UPLOAD_DIR
from app.rag.pipeline import process_file
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_TYPES:
        raise HTTPException(415, f"Unsupported file type: .{ext}")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, file.filename or f"file.{ext}")

    try:
        with open(path, "wb") as f:
            f.write(content)
        chunks = process_file(path, ext)
    finally:
        os.remove(path)

    return {"chunks": chunks, "source": file.filename or "unknown"}
