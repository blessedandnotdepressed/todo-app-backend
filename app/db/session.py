from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import get_settings


settings = get_settings()
engine = create_engine(settings.database_url)
Sessionlocal = sessionmaker(bind = engine)


def get_db() -> Generator[Session, None, None]:
    db = Sessionlocal
    try:
        yield db
    finally:
        db.close()


