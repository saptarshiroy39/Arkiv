import os, shutil
from fastapi import APIRouter, HTTPException
from app.storage.fiass import delete_vectorstore

router = APIRouter()


@router.delete("/delete")
async def delete():
    if os.path.exists("data/staging"):
        shutil.rmtree("data/staging")
    if not delete_vectorstore():
        raise HTTPException(404, "No data found")
    return {"message": "All data deleted"}
