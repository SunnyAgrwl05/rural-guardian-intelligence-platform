from sqlalchemy import text
from app.core.db import Base,engine,SessionLocal
from app.core.config import settings
from app.core.security import hash_password
from app.models import User
def init_db():
    db=SessionLocal()
    try: db.execute(text("CREATE EXTENSION IF NOT EXISTS vector")); db.commit()
    finally: db.close()
    Base.metadata.create_all(bind=engine)
    if settings.dev_seed:
        db=SessionLocal()
        if not db.query(User).filter_by(email="admin@example.com").first(): db.add(User(email="admin@example.com",password_hash=hash_password("ChangeMe!123"),role="admin")); db.commit()
        db.close()
