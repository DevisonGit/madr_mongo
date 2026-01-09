from http import HTTPStatus

from .base import DomainException


class BookAlreadyExists(DomainException):
    status_code = HTTPStatus.CONFLICT
    message = 'book already exists'


class BookNotFound(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    message = 'book not found'
