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
    allow_origins=[
        'https://bionic-reader-nu.vercel.app',
        'https://bionic-reader-1g8rrnpz2-bnzone.vercel.app',
    ],
    allow_credentials=settings.allow_credentials,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
