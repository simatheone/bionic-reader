from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentUpdate


class CRUDDocument(
    CRUDBase[
        Document,
        DocumentCreate,
        DocumentUpdate
    ]
):

    async def get_all_user_documents_with_truncated_text(
        self,
        user: User,
        session: AsyncSession
    ) -> List[Document]:
        db_obj = await session.execute(
            select(
                Document.id,
                Document.title,
                Document.text
            ).where(
                Document.user_id == user.id
            ).order_by(Document.create_date)
        )
        db_obj = db_obj.scalars().all()
        return db_obj

    async def get_document_by_title(
        self,
        document_title: str,
        session: AsyncSession
    ):
        document_id = await session.execute(
            select(
                Document.id
            ).where(Document.title == document_title)
        )
        return document_id.scalars().first()


document_crud = CRUDDocument(Document)
