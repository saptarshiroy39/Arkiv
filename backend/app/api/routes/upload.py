import os
from typing import List
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.config import ALLOWED_TYPES, MAX_FILE_SIZE

router = APIRouter()
SCHEMA = {
    "requestBody": {
        "required": True,
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "required": ["files"],
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {"type": "string", "format": "binary"},
                        }
                    },
                }
            }
        },
    }
}


@router.post("/upload", openapi_extra=SCHEMA)
async def upload(files: List[UploadFile] = File(...)):
    os.makedirs("data/staging", exist_ok=True)
    staged = []

    for f in files:
        ext = (
            (f.filename or "").split(".")[-1].lower()
            if "." in (f.filename or "")
            else ""
        )
        if ext not in ALLOWED_TYPES:
            raise HTTPException(400, f"Unsupported: {f.filename}")

        content = await f.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(413, "File too large")

        with open(os.path.join("data/staging", f.filename), "wb") as out:
            out.write(content)
        staged.append(f.filename)

    return {"staged": staged, "message": f"{len(staged)} file(s) staged"}
