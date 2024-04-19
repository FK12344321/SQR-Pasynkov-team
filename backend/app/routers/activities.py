from __future__ import annotations

from fastapi import APIRouter

from backend.app.dependencies import *

from backend.app.database import Session

router = APIRouter(tags=['activities'])


@router.post("/users/{user_id}/activities/")
def create_activity(activity: ActivityCreate, user: Annotated[User, Depends(get_current_user)]):
