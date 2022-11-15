from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_document_exists_and_user_is_owner
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.document import document_crud
from app.models import User
from app.schemas.document import (
    DocumentCreate, DocumentInfo, DocumentUpdate,
    DocumentResponse, DocumentTransformRequest
)
from app.services.text_transformation import execute_transformation_process
from app.services.pdf_generator import execute_pdf_generation_process

router = APIRouter()


@router.get(
    '/my_documents',
    response_model=Page[DocumentResponse],
    dependencies=[Depends(current_user)]
)
async def get_all_user_documents_with_truncated_text(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    params: Params = Depends()
):
    """Returns a paginated page with user's documents.

    Endpoint is available for authenticated users.

    Fields to return:
    - **items**:
        - **title**: Document's title;
        - **text**: Document's text (truncated to 30 chars).
        - **id**: Document's id.
    - **total**: total amount of documents;
    - **page**: current page number;
    - **size**: amount of documents on page.
    """
    documents = await document_crud.get_all_user_documents_with_truncated_text(
        user, session
    )
    return paginate(documents, params)


@router.get(
    '/{document_id}',
    response_model=DocumentResponse,
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
    - **title**: Document's title;
    - **text**: Document's text.
    - **id**: Document's id.
    """
    document = await check_document_exists_and_user_is_owner(
        document_id, user, session
    )
    return document


@router.get(
    '/download/{document_id}',
    dependencies=[Depends(current_user)]
)
async def download_document(
    document_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    document = await check_document_exists_and_user_is_owner(
        document_id, user, session
    )
    document_title = getattr(document, 'title')
    document_text = getattr(document, 'text')

    pdf_file_bytearray = await execute_pdf_generation_process(
        document_text
    )
    pdf_file_as_bytes = bytes(pdf_file_bytearray)
    headers = {
        'Content-Disposition': f'attachment; filename="{document_title}.pdf"'
    }
    return Response(
        content=pdf_file_as_bytes,
        headers=headers,
        media_type='application/pdf'
    )


@router.post(
    '/',
    response_model=DocumentResponse,
    response_model_exclude={'title', 'text'},
    dependencies=[Depends(current_user)],
    status_code=HTTPStatus.CREATED
)
async def create_new_document(
    document: DocumentCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Returns a user's document.
    Endpoint is available for authenticated users.

    Fields to return:
    - **id**: Document's id.
    """
    new_document = await document_crud.create(
        object_in=document, user=user, session=session
    )
    return new_document


@router.post(
    '/transform',
    response_model=DocumentResponse
)
async def transform_text(
    document: DocumentTransformRequest
):
    """Returns transfromed text as a string with html tags inside.

       Fields to return:
       - **text**: transformed text with hmtl bold tags and
       line breakes inside.
    """
    document_data = jsonable_encoder(document)
    transformed_text = None
    if document.text:
        transformed_text = await execute_transformation_process(
            document_data['text']
        )
    document_data.update({'text': transformed_text})
    return JSONResponse(content=document_data)


@router.patch(
    '/{document_id}',
    response_model=DocumentResponse,
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
    - **title**: Document's title;
    - **text**: Document's text.
    """
    document = await check_document_exists_and_user_is_owner(
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
    response_model=DocumentInfo,
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
    document = await check_document_exists_and_user_is_owner(
        document_id=document_id,
        user=user,
        session=session
    )
    document = await document_crud.remove(document, session)
    return document
