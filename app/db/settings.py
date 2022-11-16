
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Project settings."""

    # Application settings
    app_title: str = 'Bionic Reader'
    app_description: str = 'Bionic Reader'
    secret: str = 'SECRET'

    # Database settings
    db_url: str
    # postgres_db: str
    # db_host: str
    # postgres_password: str
    # db_port: str
    # postgres_user: str
    first_superuser_email: EmailStr
    first_superuser_password: str
    first_name_superuser: str

    # Cors settings
    allow_origins: str
    allow_credentials: bool
    allow_methods: str
    allow_headers: str

    # Cookie settings
    cookie_max_age: int
    cookie_name: str
    cookie_secure: bool
    cookie_httponly: bool
    cookie_samesite: str
    cookie_domain: Optional[str]

    # JWT settings
    lifetime_seconds: int

    debug: bool

    @property
    def database_url(self):
        if bool(self.debug) is True:
            return self.db_url
        # return (
        #     f"postgresql+asyncpg://"
        #     f"{self.postgres_user}:{self.postgres_password}"
        #     f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        # )

    class Config:
        env_file = '.env'


settings = Settings()
