from __future__ import annotations

from typing import List

from fastapi import APIRouter

from app.models import Error, ActivityCreate, Activity, ActivitiesRequest
from app.database.crud import create_activity, get_activities

router = APIRouter(tags=['activities'])


@router.post(
    '/activity',
    response_model=Activity,
    responses={
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
    tags=['activities'],
)
def add_activity(activity: ActivityCreate) -> Activity:
    return create_activity(activity, "user")


@router.get(
    '/activity',
    response_model=List[Activity],
    responses={
        '401': {'model': Error},
        '403': {'model': Error},
        '500': {'model': Error},
    },
    tags=['activities'],
)
def get_activity(activity_params: ActivitiesRequest) -> List[Activity]:
    return get_activities(activity_params, "user")
