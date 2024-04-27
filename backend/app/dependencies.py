from __future__ import annotations

from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic, HTTPBearer, HTTPAuthorizationCredentials  # noqa: E501

from app.internals.auth.user import check_user, get_user
from app.internals.auth.token import decode_token
from app.models import User, IncorrectUser

basic_security = HTTPBasic()
security = HTTPBearer()


async def get_current_user_basic(
        credentials: Annotated[HTTPBasicCredentials, Depends(basic_security)],
) -> User:
    if not check_user(credentials.username, credentials.password):
        raise IncorrectUser(credentials.username)
    return get_user(credentials.username)


async def get_current_user(
        token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> User:
    user = decode_token(token.credentials)
    return get_user(user.username)
