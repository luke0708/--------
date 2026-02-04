from __future__ import annotations

from pathlib import Path
from sqlmodel import SQLModel, create_engine, Session

from .config import settings


def _ensure_sqlite_path(url: str) -> None:
    if not url.startswith("sqlite:///"):
        return
    db_path = url.replace("sqlite:///", "", 1)
    path = Path(db_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)


def get_engine():
    _ensure_sqlite_path(settings.database_url)
    return create_engine(settings.database_url, connect_args={"check_same_thread": False})


engine = get_engine()


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
