from typing import List

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_document_before_edit,
                                check_document_exists_and_user_is_owner)
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.document import document_crud
from app.models import User
from app.schemas.document import DocumentCreate, DocumentDB, DocumentUpdate
from app.services.text_transformation import execute_transformation_process

router = APIRouter()


@router.get(
    '/my_documents',
    response_model=List[DocumentDB],
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
    response_model_exclude={'create_date', 'user_id'},
    dependencies=[Depends(current_user)]
)
async def get_a_single_document(
    document_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a user's document.
    Endpoint is available for the owner of the document.

    Fields to return:
    - **id**: Document id;
    - **title**: Document title;
    - **text**: Document text.
    """
    document = await check_document_exists_and_user_is_owner(
        document_id, user, session
    )
    return document


@router.post(
    '/',
    response_model=DocumentDB,
    response_model_exclude={
        'title', 'text', 'create_date', 'user_id'
    },
    dependencies=[Depends(current_user)]
)
async def create_new_document(
    document: DocumentCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a user's document.
    Endpoint is available for authenticated users.

    Fields to return:
    - **id**: Document id.
    """
    new_document = await document_crud.create(
        object_in=document, user=user, session=session
    )
    return new_document


@router.post('/transform')
async def transform_text(
    text_to_transform: str = Body(example={'text': 'Text to transform'})
):
    """Returns transfromed text as a string with html tags inside."""
    transformed_text = await execute_transformation_process(
        text_to_transform
    )
    return {'text': transformed_text}


@router.patch(
    '/{document_id}',
    response_model=DocumentDB,
    response_model_exclude={'user_id', 'create_date'},
    dependencies=[Depends(current_user)]
)
async def partially_update_document(
    document_id: int,
    object_in: DocumentUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a patched document.
    Endpoint is available for the owner of the document.

    Fields to return:
    - **title**: Document title;
    - **text**: Document text;
    - **id**: Document id;
    - **create_date**: Document create date;
    - **user_id**: User id related to the document.
    """
    document = await check_document_before_edit(
        document_id=document_id,
        user=user,
        session=session
    )
    document = await document_crud.update(
        db_object=document,
        object_in=object_in,
        session=session
    )
    return document


@router.delete(
    '/{document_id}',
    response_model=DocumentDB,
    dependencies=[Depends(current_user)]
)
async def delete_document(
    document_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a deleted document.
    Endpoint is available for the owner of the document.

    Fields to return:
    - **title**: Document title;
    - **text**: Document text;
    - **id**: Document id;
    - **create_date**: Document create date;
    - **user_id**: User id related to the document.
    """
    document = await check_document_before_edit(document_id, user, session)
    document = await document_crud.remove(document, session)
    return document
