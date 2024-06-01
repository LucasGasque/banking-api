from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):
    APP_NAME: str = "Banking-API"
    ENVIROMENT: str = "development"

    JWT_SECRET_KEY: str = "very_secret_key_plz_change_it"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = __Settings()  # type: ignore
