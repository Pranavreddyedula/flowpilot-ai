from __future__ import annotations

from pathlib import Path

import pytest

from backend.app.storage.db import Base, DATABASE_PATH, close_db, engine


@pytest.fixture(autouse=True)
def reset_database() -> None:
    close_db()
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
    Base.metadata.create_all(bind=engine)
    yield
    close_db()
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()
