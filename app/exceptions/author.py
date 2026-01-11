from http import HTTPStatus

from .base import DomainException


class AuthorAlreadyExists(DomainException):
    status_code = 409
    message = 'author already exists'


class AuthorNotFound(DomainException):
    status_code = HTTPStatus.NOT_FOUND
    message = 'author not found'


class AuthorInvalidId(DomainException):
    status_code = HTTPStatus.BAD_REQUEST
    message = 'id of author invalid'
