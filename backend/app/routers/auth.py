from __future__ import annotations

from typing import Union, Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_current_user_basic, get_current_user
from app.models import User, UserCredentials, Error
from app.internals.auth import token, user as auth_user

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
def login(
        user: Annotated[User, Depends(get_current_user_basic)],
) -> Union[UserCredentials, Error]:
    """
    Login user
    """
    return token.generate_token_from_user(user)


@router.post(
    '/auth/register',
    response_model=UserCredentials,
    responses={
        '400': {'model': Error},
        '500': {'model': Error},
    },
    tags=['auth'],
)
def register(user: User) -> Union[UserCredentials, Error]:
    """
    Register user
    """
    if auth_user.is_exist(user.username):
        return JSONResponse(
            status_code=400,
            content=Error(
                message='User is already registered',
                description='User with this name already exists',
            ).model_dump(mode='json')
        )
    new_user = auth_user.create_user(user)
    return token.generate_token_from_user(new_user)


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
def refresh_token(
        user: Annotated[User, Depends(get_current_user)],
) -> Union[UserCredentials, Error]:
    """
    Refresh token
    """
    return token.generate_token_from_user(user)
