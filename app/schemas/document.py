from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Extra, Field


class DocumentBaseSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    text: Optional[str] = Field(None, min_length=1)

    class Config:
        extra = Extra.forbid


class DocumentCreate(DocumentBaseSchema):
    title: str = Field(
        'Untitled Document',
        min_length=1,
        max_length=256
    )
    text: str = Field('Enter your text', min_length=1)


class DocumentUpdate(DocumentBaseSchema):
    pass


class DocumentTransformRequest(BaseModel):
    text: str = Field(min_length=1)


class DocumentInfo(DocumentCreate):
    id: UUID
    create_date: datetime
    user_id: Optional[UUID]

    class Config:
        orm_mode = True


class DocumentResponse(DocumentCreate):
    id: UUID

    class Config:
        orm_mode = True
