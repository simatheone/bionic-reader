from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_document_exists
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.document import document_crud
from app.models import User
from app.schemas.document import DocumentDB

router = APIRouter()


@router.get(
    '/my_documents',
    response_model=list[DocumentDB],
    response_model_exclude={'create_date', 'user_id'},
    dependencies=[Depends(current_user)]
)
async def get_all_user_documents_with_truncated_text(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a list with all user's documents.
    Endpoint is available for authenticated users.

    Fields to return:
    - **id**: Document id;
    - **title**: Document title;
    - **text**: Document text (truncated to 30 chars).
    """
    return await document_crud.get_all_user_documents_with_truncated_text(
        user, session
    )


@router.get(
    '/{document_id}',
    response_model=DocumentDB,
    dependencies=[Depends(current_user)]
)
async def get_a_single_document(
    document_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    document = await check_document_exists(
        document_id, session
    )
    return document


@router.post('/')
async def create_document():
    ...


@router.patch(
    '/{document_id}'
)
async def partially_update_document():
    ...


@router.delete(
    '/{document_id}',
    response_model=DocumentDB,
    dependencies=[Depends(current_user)]
)
async def delete_document(
    document_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a deleted document.
    Endpoint is available for authenticated users.

    Fields to return:
    - **title**: Document title;
    - **text**: Document text;
    - **id**: Document id;
    - **create_date**: Document create date;
    - **user_id**: User id related to the document.
    """
    document = await check_document_exists(document_id, session)
    document = await document_crud.remove(document, session)
    return document
