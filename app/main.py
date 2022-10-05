from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins.split(','),
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods.split(','),
    allow_headers=settings.allow_headers.split(',')
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
