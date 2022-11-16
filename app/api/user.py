from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.db.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth',
    tags=['Authorization']
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Authorization']
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['Password']
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['Users']
)


@router.patch(
    '/users/{id}',
    tags=['Users'],
    deprecated=True
)
def patch_user(id: str):
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail='Patching users is not allowed'
    )


@router.delete(
    '/users/{id}',
    tags=['Users'],
    deprecated=True
)
def delete_user(id: str):
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail='Deleting users is not allowed'
    )
