from pydantic import Field
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    first_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., min_length=1, max_length=128)


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str | None
