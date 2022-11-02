from typing import List

from sqlalchemy import select, desc, func
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
                Document.id,
                Document.title,
                func.substr(Document.text, 1, 30).label('text')
            ).where(
                Document.user_id == user.id,
            ).order_by(desc(Document.create_date))
        )
        db_object = db_object.all()
        print(db_object)

        return db_object


document_crud = CRUDDocument(Document)
