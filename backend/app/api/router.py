from app.api.routes.ask import router as ask_router
from app.api.routes.default import router as default_router
from app.api.routes.delete import router as delete_router
from app.api.routes.process import router as process_router
from app.api.routes.upload import router as upload_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(default_router)
router.include_router(upload_router)
router.include_router(process_router)
router.include_router(ask_router)
router.include_router(delete_router)
