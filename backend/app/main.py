from app.routes.ask import router as ask_router
from app.routes.delete import router as delete_router
from app.routes.upload import router as upload_router
from app.config import APP_NAME, APP_VERSION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Arkiv - RAG Application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_router)
app.include_router(upload_router)
app.include_router(delete_router)


@app.get("/")
async def root():
    return {"name": APP_NAME, "version": APP_VERSION, "status": "ok"}


# Manual
