from __future__ import annotations

from fastapi import APIRouter

from backend.app.dependencies import *
from backend.app.models import UserCredentials, Error, ActivityCreate
from backend.app.database.crud import create_activity

router = APIRouter(tags=['activities'])


@router.get(
    '/auth/login',
    response_model=ActivityCreate,
    responses={
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
    tags=['auth'],
)
def create_activity(activity: ActivityCreate, user: Annotated[User, Depends(get_current_user)]):
    return create_activity(activity, user.username)