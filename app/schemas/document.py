from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Extra, Field


class ORMMode(BaseModel):
    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    text: Optional[str] = Field(None, min_length=1)

    class Config:
        extra = Extra.forbid


class DocumentCreate(DocumentBase):
    title: str = Field(
        'Untitled Document',
        min_length=1,
        max_length=256
    )
    text: str = Field('Enter your text', min_length=1)


class DocumentTransformRequest(BaseModel):
    text: str = Field(min_length=1)


class DocumentResponse(DocumentCreate, ORMMode):
    id: UUID


class DocumentInfo(DocumentResponse):
    created_at: datetime
    user_id: Optional[UUID]
