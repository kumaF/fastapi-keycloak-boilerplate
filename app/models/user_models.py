from typing import List, Optional
from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pydantic.class_validators import validator
from pydantic import (
    BaseModel,
    Field
)

from .project_models import (
    SubtitleProject,
)

class BaseUser(BaseModel):
    email: str = Field(...)
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)


class MongoUser(BaseUser):
    user_id: str = Field(...)
    subtitle_projects: List[SubtitleProject] = Field([])
    stream_projects: list = Field([])
    transcord_projects: list = Field([])

class User(BaseUser):
    password: str = Field(...)

    @validator('username')
    def validate_username(cls, v):
        if v == '':
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username field is required"
            )
        return v

    @validator('email')
    def validate_email(cls, v):
        if v == '':
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email field is required"
            )
        return v

    @validator('password')
    def validate_password(cls, v):
        if v == '':
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password field is required"
            )
        return v


class LoginUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

    @validator('email', always=True)
    def validate_username(cls, email, values):
        username = values.get('username', None)

        if (email is None or email == '') and (username is None or username == ''):
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Either email or username is required"
            )
        return email

    @validator('password')
    def validate_password(cls, password):
        if password == '' or password is None:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password field is required"
            )
        return password


class UpdateUser(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    subtitle_projects: List[SubtitleProject] = None
    stream_projects: list = None
    transcording_projects: list = None

class OutUser(BaseModel):
    user_id: str = Field(...)
    username: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    # subtitle_projects: List[OutUserSubtitleProject] = Field([])
    # stream_projects: list = Field([])
    # transcording_projects: list = Field([])
