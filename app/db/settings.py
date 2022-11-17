from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """Project settings."""

    # Application settings
    APP_TITLE: str = 'Bionic Reader'
    APP_DESCRIPTION: str = 'Bionic Reader'
    SECRET: str = 'SECRET'

    # Database settings
    PGDATABASE: str
    PGHOST: str
    PGPASSWORD: str
    PGPORT: str
    PGUSER: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_NAME_SUPERUSER: str

    # Cors settings
    ALLOW_ORIGINS: str
    ALLOW_CREDENTIALS: bool
    ALLOW_METHODS: str
    ALLOW_HEADERS: str

    # Cookie settings
    COOKIE_MAX_AGE: int
    COOKIE_NAME: str
    COOKIE_SECURE: bool
    COOKIE_HTTPONLY: bool
    COOKIE_SAMESITE: str

    # JWT settings
    LIFETIME_SECONDS: int

    @property
    def database_url(self):

        return (
            f"postgresql+asyncpg://"
            f"{self.PGUSER}:{self.PGPASSWORD}"
            f"@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"
        )

    class Config:
        env_file = '.env'


settings = Settings()
