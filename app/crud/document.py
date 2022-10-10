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
        db_object = await session.execute(
            select(
                Document
            ).where(
                Document.user_id == user.id,
            ).order_by(Document.create_date)
        )
        db_object = db_object.scalars().all()

        for _ in db_object:
            if len(_.text) > 30:
                _.text = _.text[:30] + '...'

        return db_object


document_crud = CRUDDocument(Document)
