from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.document import document_crud
from app.models import Document
from app.models.user import User


async def check_document_exists_and_user_is_owner(
    document_id: int,
    user: User,
    session: AsyncSession
) -> Document:
    document = await document_crud.get(
        object_id=document_id, session=session
    )
    if not document:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'The Document with id "{document_id}" is not found'
        )

    if document.user_id != User.id or not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Only the owner of the document is allowed to get it'
        )
    return document


async def check_document_before_edit(
    document_id: int,
    user: User,
    session: AsyncSession
):
    document = await document_crud.get(document_id, session)

    if not document:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'The Document with id "{document_id}" is not found'
        )

    if document.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You can not modify others\' documents!'
        )
    return document
