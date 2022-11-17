from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[UUID]):
    first_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., min_length=1, max_length=128)


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
