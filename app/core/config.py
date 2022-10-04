from typing import Optional, List, Sequence

from pydantic import BaseSettings, EmailStr

ENV_FILE = '.env'


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
    # allow_origins: Optional[Sequence[str]]
    # allow_credentials: Optional[bool]
    # allow_methods: Optional[List[str]]
    # allow_headers: Optional[List[str]]

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
        env_file = f'{ENV_FILE}'


settings = Settings()   # pyright: ignore
