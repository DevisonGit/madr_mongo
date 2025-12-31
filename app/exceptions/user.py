from .base import DomainException


class UserNotFound(DomainException):
    status_code = 404
    message = 'user not found'


class UserAlreadyExists(DomainException):
    status_code = 409
    message = 'user already exists'
