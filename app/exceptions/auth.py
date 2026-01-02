from http import HTTPStatus

from .base import DomainException


class AuthUnauthorized(DomainException):
    status_code = HTTPStatus.UNAUTHORIZED
    message = 'incorrect email or password'


class AuthCredentialsValidate(DomainException):
    status_code = HTTPStatus.UNAUTHORIZED
    message = 'could not validate credentials'
