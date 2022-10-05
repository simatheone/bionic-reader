from typing import Optional

from pydantic import BaseSettings, EmailStr

ENV_FILE = '.env.dev'


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
    # fix this settings. Pydantic couldn't parse them.
    # allow_origins: Optional[Sequence[str]]
    allow_credentials: bool = False
    # allow_methods: Optional[List[str]]
    # allow_headers: list

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


settings = Settings()    # pyright: ignore
