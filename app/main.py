import logging.config

from fastapi import FastAPI

from app.api.v1.routers import router as router_v1
from app.core.exception_handlers import (
    domain_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging import LOGGING_CONFIG
from app.exceptions.base import DomainException

logging.config.dictConfig(LOGGING_CONFIG)
app = FastAPI()


app.include_router(router_v1, prefix='/api/v1')


app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
