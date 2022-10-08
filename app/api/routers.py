from fastapi import APIRouter

from app.api.endpoint import document_router, user_router

main_router = APIRouter()

main_router.include_router(
    document_router,
    prefix='/document',
    tags=['Documents']
)

main_router.include_router(user_router)
