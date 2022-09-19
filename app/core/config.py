from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Bionic Reader'
    app_description: str = 'Bionic Reader'
    database_url: str | None
    secret: str = 'SECRET'
    first_superuser_email: EmailStr | None
    first_superuser_password: str | None
    first_name_superuser: str | None

    class Config:
        env_file = '.env'


settings = Settings()   # pyright: ignore
