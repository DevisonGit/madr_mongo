from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_root_user: str
    mongo_root_password: str
    mongo_db: str
    mongo_host: str
    mongo_port: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def mongodb_url(self) -> str:
        return (
            f'mongodb://{self.mongo_root_user}:'
            f'{quote_plus(self.mongo_root_password)}@'
            f'{self.mongo_host}:{self.mongo_port}/'
            f'?authSource=admin'
        )


settings = Settings()
