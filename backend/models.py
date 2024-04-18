# generated by fastapi-codegen:
#   filename:  ./api/api.swagger.yaml
#   timestamp: 2024-04-18T23:37:43+00:00

from __future__ import annotations

from typing import Optional

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
