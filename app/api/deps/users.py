from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode

from app.api.deps.sevice import AuthServiceDep
from app.core.settings import settings
from app.exceptions.auth import AuthCredentialsValidate

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token', refreshUrl='auth/refresh'
)
Token = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(service: AuthServiceDep, token: Token):
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise AuthCredentialsValidate()
    except DecodeError:
        raise AuthCredentialsValidate()
    except ExpiredSignatureError:
        raise AuthCredentialsValidate()

    user = await service.validate_current_user(subject_email)

    return user
