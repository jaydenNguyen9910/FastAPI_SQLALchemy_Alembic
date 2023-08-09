from typing import Optional, Dict, List
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator, FieldValidationInfo


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI_SQLALchemy_Alembic example"
    PROJECT_DESCRIPTION: str = """Example for FastAPI_SQLALchemy_Alembic setup 🚀"""
    PROJECT_TAGS_METADATA: List[Dict[str, str]] = [
        {
            "name": "login/logout",
            "description": "There are 2 options to transport the token, via request headers and cookie.",
        },
        {
            "name": "registration",
            "description": "Create new account. Email verification is required.",
        },
        {
            "name": "verification",
            "description": "Verification token is sent to user through email.",
        },
        {
            "name": "password management",
            "description": "Verification token is sent to user through email.",
        },
        {
            "name": "oauth2",
            "description": "'authorized' endpoint: get google info "
                           "==return==google==info==> 'redirect' url: your website "
                           "==paste==google==info==> 'callback' endpoint: create user and return cookie "
                           "==cookie==> 'redirect' url",
        },
    ]
    API_PREFIX: str = "/api"
    VERSION: str = "0.1-SNAPSHOT"
    ALLOW_ORIGINS: list = ["*"]
    DEBUG: bool = False
    SQLALCHEMY_DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str
    DATABASE_URL: str
    PROJECT_BUILD_TYPE: Optional[str] = None
    JWT_SECRET: str
    SYSTEM_EMAIL: str
    SYSTEM_EMAIL_PASSWORD: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
