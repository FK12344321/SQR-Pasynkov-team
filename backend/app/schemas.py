from pydantic import BaseModel


class UserCreate(BaseModel):
    nickname: str


class UserResponse(BaseModel):
    id: int
    nickname: str


class ActivityCreate(BaseModel):
    activity_time: str
    start_date: str
    end_date: str
