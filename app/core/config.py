from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Bionic Reader'
    app_description: str = 'Bionic Reader'
    database_url: str = 'Bionic Reader'

    class Config:
        env_file = '.env'


settings = Settings()
