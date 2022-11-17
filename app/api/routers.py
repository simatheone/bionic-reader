from fastapi import APIRouter

from app.api.document import router as document_router
from app.api.user import router as user_router

main_router = APIRouter()

main_router.include_router(document_router)
main_router.include_router(user_router)
