import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from app.api.v1.routers import router as router_v1
from app.core.exception_handlers import (
    domain_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging import LOGGING_CONFIG
from app.core.settings import settings
from app.db.indexes import create_indexes
from app.exceptions.base import DomainException


@asynccontextmanager
async def db_lifespan(app: FastAPI):
    app.mongodb_client = AsyncMongoClient(settings.mongodb_url)
    app.database = app.mongodb_client['madr']
    await create_indexes(app.database)
    yield
    await app.mongodb_client.close()


logging.config.dictConfig(LOGGING_CONFIG)
app = FastAPI(lifespan=db_lifespan)


app.include_router(router_v1, prefix='/api/v1')


app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
