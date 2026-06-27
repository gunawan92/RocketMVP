import os
from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

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
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://127.0.0.1:3000,http://localhost:3000")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def sqlalchemy_database_url(self) -> str:
        database_url = self.database_url
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        if database_url.startswith("postgresql+psycopg://"):
            return self._without_unsupported_psycopg_options(database_url)
        return database_url

    @staticmethod
    def _without_unsupported_psycopg_options(database_url: str) -> str:
        parsed = urlsplit(database_url)
        query_items = [(key, value) for key, value in parse_qsl(parsed.query) if key != "channel_binding"]
        query_keys = {key for key, _ in query_items}
        host = parsed.hostname or ""
        if host.endswith(".neon.tech") and "options" not in query_keys:
            endpoint_id = host.split(".", 1)[0]
            query_items.append(("options", f"endpoint={endpoint_id}"))
        query = urlencode(query_items)
        return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
