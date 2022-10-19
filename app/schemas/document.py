from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


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
    text: str = Field(..., min_length=1)

    @validator('title')
    def validate_title_on_create(cls, title_value: str):
        if not title_value:
            raise ValueError('The "title" of the document can not be empty')
        if len(title_value) > 256:
            raise ValueError(
                'The length of the "title" can not be more then 256 characters'
            )
        return title_value

    @validator('text')
    def validate_text_on_create(cls, text_value: str):
        if text_value is None:
            raise ValueError('The "text" of the document can not be empty')
        return text_value


class DocumentUpdate(DocumentBaseSchema):
    pass

    # fix: get rid of repetion
    # make 1 reuseable validator
    @validator('title')
    def validate_title_on_update(cls, title_value: Optional[str]):
        if title_value is None:
            raise ValueError('The "title" of the document can not be empty')
        return title_value

    @validator('text')
    def validate_text_on_update(cls, text_value: Optional[str]):
        if text_value is None:
            raise ValueError('The "text" of the document can not be empty')
        return text_value


class DocumentDB(DocumentCreate):
    id: int
    create_date: datetime
    user_id: Optional[int]

    class Config:
        orm_mode = True
