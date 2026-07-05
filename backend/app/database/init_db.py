from app.database import base
from app.database.session import engine


def init_db() -> None:
    base.Base.metadata.create_all(bind=engine)
