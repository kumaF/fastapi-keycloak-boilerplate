from typing import List, Optional
from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pydantic.class_validators import validator
from pydantic import (
    BaseModel,
    Field
)

class JobModel(BaseModel):
    job_id: str
    job_type: str

class ProjectBaseModel(BaseModel):
    id: str
    name: str
    created_time: str
    updated_time: str
    type: str
    is_delete: bool = Field(False)

class OutProjectsModel(BaseModel):
    projects: List[ProjectBaseModel]
    
class SubtitleProject(ProjectBaseModel):
    resources: list = Field([])
    jobs: List[JobModel] = Field([])

class StreamProject(ProjectBaseModel):
    stacks: list = Field([])

class UpdateProjectModel(BaseModel):
    name: str