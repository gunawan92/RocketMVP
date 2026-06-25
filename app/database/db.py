from app.core.config import get_settings
from app.database.session import check_database_connection, get_db, get_engine, get_session_factory


def get_database_url() -> str:
    return get_settings().sqlalchemy_database_url


__all__ = [
    "check_database_connection",
    "get_database_url",
    "get_db",
    "get_engine",
    "get_session_factory",
]
