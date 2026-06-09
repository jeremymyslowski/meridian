from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://meridian:meridian@localhost:5432/meridian"
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()