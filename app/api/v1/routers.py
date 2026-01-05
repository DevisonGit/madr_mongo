from fastapi import APIRouter

from .endpoint import auth, health, users, author

router = APIRouter()

router.include_router(health.router, prefix='/health', tags=['health'])
router.include_router(users.router, prefix='/users', tags=['users'])
router.include_router(auth.router, prefix='/auth', tags=['auth'])
router.include_router(author.router,  prefix='/authors', tags=['authors'])
