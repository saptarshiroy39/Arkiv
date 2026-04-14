from app.rag.vectorstore import delete_vectorstore
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.delete("/delete")
async def delete_index() -> dict:
    if not delete_vectorstore():
        raise HTTPException(404, "No vector store found.")
    return {"message": "Vector store deleted."}
