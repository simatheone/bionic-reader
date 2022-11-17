from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.document import DocumentCreate, DocumentUpdate

from .models import Document, User


class CRUDDocument:
    def __init__(self, model):
        self.model = model

    async def get(
        self,
        document_id: UUID,
        session: AsyncSession
    ) -> Optional[Document]:
        db_document = await session.execute(
            select(self.model).where(
                Document.id == document_id
            )
        )
        return db_document.scalars().first()

    async def create(
        self,
        document_in: DocumentCreate,
        session: AsyncSession,
        user: User
    ) -> Document:
        document_in_data = document_in.dict()
        document_in_data['user_id'] = user.id

        db_object = Document(**document_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def update(
        self,
        db_document: Document,
        document_update: DocumentUpdate,
        session: AsyncSession
    ) -> Document:
        document_data = jsonable_encoder(db_document)
        document_update_data = document_update.dict(exclude_unset=True)

        for field in document_data:
            if field in document_update_data:
                setattr(db_document, field, document_update_data[field])
        session.add(db_document)
        await session.commit()
        await session.refresh(db_document)
        return db_document

    async def remove(
        self,
        document: Document,
        session: AsyncSession
    ) -> Document:
        await session.delete(document)
        await session.commit()
        return document

    async def get_all_user_documents_with_truncated_text(
        self,
        user: User,
        session: AsyncSession
    ) -> List[Document]:
        db_documents = await session.execute(
            select(
                self.model.id,
                self.model.title,
                func.substr(self.model.text, 1, 30).label('text')
            ).where(
                self.model.user_id == user.id,
            ).order_by(desc(self.model.created_at))
        )
        db_documents = db_documents.all()
        return db_documents


document_crud = CRUDDocument(Document)
