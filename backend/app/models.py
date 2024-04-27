from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, constr


class Error(BaseModel):
    message: str = Field(None, description='Simple message for user')
    description: str = Field(
        None, description='Technical description of the problem'
    )


class User(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=5) = Field(..., description="User's password")


class UserCredentials(BaseModel):
    access_token: str
    refresh_token: str


class ActivityCreate(BaseModel):
    activity_type: str
    start_date: datetime
    end_date: datetime


class Activity(BaseModel):
    activity_type: str
    start_date: datetime
    end_date: datetime
    id: int


class ActivitiesFilter(BaseModel):
    page_index: int = Field(ge=1)
    page_size: int
    activity_type: Optional[constr(min_length=1)]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class IncorrectUser(Exception):
    def __init__(self, username: str):
        self.username = username


class IncorrectToken(Exception):
    def __init__(self, token_type: str):
        self.token_type = token_type
