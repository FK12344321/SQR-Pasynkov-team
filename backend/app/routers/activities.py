from __future__ import annotations

from slowapi import limiter
from typing import List, Annotated, Optional
from datetime import datetime

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models import ActivityCreate, Activity, ActivitiesFilter, User, Error
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
@limiter.limit("200/minute")
def add_activity(
        user: Annotated[User, Depends(get_current_user)],
        activity: ActivityCreate,
) -> Activity:
    return create_activity(activity, user.username)


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
@limiter.limit("50/minute")
def get_activity_list(
        user: Annotated[User, Depends(get_current_user)],
        page_index: int,
        page_size: int,
        activity_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
) -> List[Activity]:
    return get_activities(ActivitiesFilter(
        page_index=page_index,
        page_size=page_size,
        activity_type=activity_type,
        start_date=start_date,
        end_date=end_date,
    ), user.username)
