from fastapi import APIRouter

from app.schemas.message import Message

router = APIRouter()


@router.get('/', response_model=Message)
async def health():
    return {'message': 'ok'}
