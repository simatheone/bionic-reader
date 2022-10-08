from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.document import document_crud
from app.models import Document
from app.models.user import User


async def check_document_exists(
    document_id: int,
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
    return document


async def check_document_title_duplicate(
    document_title: str,
    session: AsyncSession
) -> None:
    document_id = await document_crud.get_document_by_title(
        document_title, session
    )

    if document_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'The Document with title "{document_title}" ',
                'is already exist. Enter another unique title ',
                'for the document.',
            )
        )


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
            status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            detail='You can not modify others\' documents!'
        )
    return document
