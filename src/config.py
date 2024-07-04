from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str

    @property
    def url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    echo: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    db: DatabaseConfig


settings = Settings()
