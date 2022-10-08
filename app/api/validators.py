from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.document import document_crud
from app.models import Document


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
            detail=f'Document with id "{document_id}" is not found'
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
