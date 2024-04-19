# generated by fastapi-codegen:
#   filename:  api.swagger.yaml
#   timestamp: 2024-04-18T23:37:43+00:00

from __future__ import annotations

from typing import Union

from fastapi import APIRouter

from backend.app.dependencies import *
from backend.app.models import UserCredentials, Error

router = APIRouter(tags=['auth'])


@router.get(
    '/auth/login',
    response_model=UserCredentials,
    responses={
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
    tags=['auth'],
)
def login(user: Annotated[User, Depends(get_current_user_basic)]) -> Union[UserCredentials, Error]:
    """
    Login user
    """
    return UserCredentials(access_token=user.username, refresh_token=user.password)


@router.post(
    '/auth/register',
    response_model=UserCredentials,
    responses={'400': {'model': Error}, '500': {'model': Error}},
    tags=['auth'],
)
def register(body: User) -> Union[UserCredentials, Error]:
    """
    Register user
    """
    return Error(message='User is already registered')


@router.get(
    '/auth/token',
    response_model=UserCredentials,
    responses={
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
    tags=['auth'],
)
def refresh_token(user: Annotated[User, Depends(get_current_user)]) -> Union[UserCredentials, Error]:
    """
    Refresh token
    """
    return UserCredentials(access_token=user.username, refresh_token=user.password)
