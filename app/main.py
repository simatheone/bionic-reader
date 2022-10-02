import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser

load_dotenv()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)

origins = os.getenv('ORIGINS').split(', ')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=os.getenv('ALLOW_CREDENTIALS'),
    allow_methods=os.getenv('ALLOW_METHODS').split(','),
    allow_headers=os.getenv('ALLOW_HEADERS').split(',')
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
