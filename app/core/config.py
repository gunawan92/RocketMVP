import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel


def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#") or "=" not in cleaned:
            continue
        key, value = cleaned.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Rocket Mission Planner")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("APP_DEBUG", "true").lower() in {"1", "true", "yes", "on"}
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./rocket_mission_planner.db")
    g0: float = float(os.getenv("STANDARD_GRAVITY", "9.80665"))

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return self.database_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
