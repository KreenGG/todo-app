from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class DatabaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db: str
    
    @property
    def database_url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
    
    echo: bool = True

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = 'src/.env',
        case_sensitive=False,
        env_nested_delimiter="__",
        # env_prefix="APP__",
    )
    
    db: DatabaseConfig

settings = Settings()
