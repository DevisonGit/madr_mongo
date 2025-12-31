import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base import DomainException

logger = logging.getLogger('app.domain')


async def domain_exception_handler(request: Request, exc: DomainException):
    log_method = getattr(logger, exc.log_level, logger.warning)

    log_method(
        'Domain error',
        extra={
            'path': request.url.path,
            'method': request.method,
            'error': exc.message,
        },
    )

    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        'Unhandled exception',
        extra={'path': request.url.path, 'method': request.method},
    )

    return JSONResponse(
        status_code=500, content={'error': 'Internal server error'}
    )
