from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_ROOT_USER: str
    MONGO_ROOT_PASSWORD: str
    MONGO_DB: str
    MONGO_HOST: str
    MONGO_PORT: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def mongodb_url(self) -> str:
        return (
            f'mongodb://{self.MONGO_ROOT_USER}:'
            f'{quote_plus(self.MONGO_ROOT_PASSWORD)}@'
            f'{self.MONGO_HOST}:{self.MONGO_PORT}/'
            f'?authSource=admin'
        )


settings = Settings()
