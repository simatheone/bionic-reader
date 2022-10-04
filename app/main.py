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
        'https://bionic-reader-production.up.railway.app',
        'https://bionic-reader-1g8rrnpz2-bnzone.vercel.app',
        'https://bionic-reader-nu.vercel.app',
        'http://localhost',
        'http://localhost:8080',
        'http://localhost:3000',
        'http://127.0.0.1:8000'
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
