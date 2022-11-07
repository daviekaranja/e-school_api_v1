import secrets

from pydantic import BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PROJECT_NAME: str = "E-School"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "1256"
    POSTGRES_DATABASE_NAME: str = "db"
    SCHEME: str = "postgresql"

    FIRST_SUPERUSER_EMAIL: EmailStr = "admin@eschool.com"
    FIRST_SUPERUSER_PASSWORD: str = "password"
    USERS_OPEN_REGISTRATION: bool = False

    sqlalchemy_url = 'postgresql://postgres:1256@localhost/db'

    class Config:
        case_sensitive = True


settings = Settings()
