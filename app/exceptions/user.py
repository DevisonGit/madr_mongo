from http import HTTPStatus

from .base import DomainException


class UserNotFound(DomainException):
    status_code = 404
    message = 'user not found'


class UserAlreadyExists(DomainException):
    status_code = 409
    message = 'user already exists'


class UserInvalidId(DomainException):
    status_code = HTTPStatus.BAD_REQUEST
    message = 'id of user invalid'
