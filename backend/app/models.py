from __future__ import annotations

from typing import Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field, constr


class Error(BaseModel):
    message: Optional[str] = Field(None, description='Simple message for user')
    description: Optional[str] = Field(
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


class ActivitiesRequest(BaseModel):
    page_index: int
    page_size: int
    activity_type: Union[str, None]
    start_date: Union[datetime, None]
    end_date: Union[datetime, None]


class IncorrectUser(Exception):
    def __init__(self, username: str):
        self.username = username


class IncorrectToken(Exception):
    def __init__(self, token_type: str):
        self.token_type = token_type
