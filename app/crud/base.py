from typing import Generic, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=Optional[BaseModel])


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self,
        object_id: int,
        session: AsyncSession
    ) -> Optional[ModelType]:
        db_object = await session.execute(
            select(self.model).where(
                self.model.id == object_id
            )
        )
        return db_object.scalars().first()

    async def get_multi(self):
        pass

    async def create(
        self,
        object_in,
        session: AsyncSession,
        user: User
    ) -> ModelType:
        object_in_data = object_in.dict()
        object_in_data['user_id'] = user.id

        db_object = self.model(**object_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def update(
        self,
        db_object,
        object_in,
        session: AsyncSession
    ) -> ModelType:
        object_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)

        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(
        self,
        db_object,
        session: AsyncSession
    ) -> ModelType:
        await session.delete(db_object)
        await session.commit()
        return db_object
