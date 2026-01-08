from http import HTTPStatus

from .base import DomainException


class BookAlreadyExists(DomainException):
    status_code = HTTPStatus.CONFLICT
    message = 'book already exists'
