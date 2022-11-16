from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud_document import document_crud
from app.models import Document, User


async def check_document_exists_and_user_is_owner(
    document_id: UUID,
    user: User,
    session: AsyncSession
) -> Document:
    document = await document_crud.get(
        document_id=document_id,
        session=session
    )
    if not document:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The Document with id "{document_id}" is not found'
        )
    if document.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Only the owner of the document is allowed to view it'
        )
    return document
