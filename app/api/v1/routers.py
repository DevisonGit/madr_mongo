from fastapi import APIRouter

from .endpoint import health

router = APIRouter()

router.include_router(health.router, prefix='/health', tags=['health'])
