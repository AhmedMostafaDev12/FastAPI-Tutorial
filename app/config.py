from pydantic_settings import SettingsConfigDict, BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_username: str 
    database_password: str 
    database_hostname: str 
    database_port: str 
    database_name: str 
    secret_key: str
    algorithm: str 
    access_token_expire_minutes: int 

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()