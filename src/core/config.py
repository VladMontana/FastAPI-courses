from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# ------PATHS------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    JWT_SECRET_KEY: str
    JWT_ALGORITM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")
    # extra="ignore" - это игнорирование лишних значений в .env

    REDIS: str

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS}"


settings = Settings()
