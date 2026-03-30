from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Arkiv API", "version": "0.1", "status": "OK"}
