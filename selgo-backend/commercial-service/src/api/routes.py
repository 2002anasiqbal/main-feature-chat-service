from fastapi import APIRouter
from .commercial_routes import router as commercial_router

router = APIRouter()
router.include_router(commercial_router)