from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    # Application settings
    app_title: str = 'Bionic Reader'
    app_description: str = 'Bionic Reader'
    secret: str = 'SECRET'

    # Database settings
    database_url: Optional[str]
    pgdatabase: Optional[str]
    pghost: Optional[str]
    pgpassword: Optional[str]
    pgport: Optional[str]
    pguser: Optional[str]
    first_superuser_email: Optional[EmailStr]
    first_superuser_password: Optional[str]
    first_name_superuser: Optional[str]

    # Cors settings
    allow_origins: str
    allow_credentials: bool = False
    allow_methods: str
    allow_headers: str

    # Cookie settings
    cookie_max_age: Optional[int]
    cookie_name: str = 'cookie-auth'
    cookie_secure: bool = False
    cookie_httponly: bool = False
    cookie_samesite: str = 'lax'
    cookie_domain: Optional[str]

    # JWT settings
    lifetime_seconds: Optional[int]

    class Config:
        env_file = '.env'


settings = Settings()    # pyright: ignore
