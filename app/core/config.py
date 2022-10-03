from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Bionic Reader'
    app_description: str = 'Bionic Reader'
    database_url: Optional[str]
    pgdatabase: Optional[str]
    pghost: Optional[str]
    pgpassword: Optional[str]
    pgport: Optional[str]
    pguser: Optional[str]
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr]
    first_superuser_password: Optional[str]
    first_name_superuser: Optional[str]

    class Config:
        env_file = '.env'


settings = Settings()   # pyright: ignore
