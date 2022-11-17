from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import main_router
from app.db.init_db import create_first_superuser
from app.db.settings import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS.split(','),
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS.split(','),
    allow_headers=settings.ALLOW_HEADERS.split(',')
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
