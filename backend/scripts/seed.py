import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, SessionLocal, engine
from app.services.auth_service import create_default_admin
from app.services.doc_ingestion import ingest_all_docs
from sqlalchemy import text


def seed():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = create_default_admin(db)
        if admin:
            print(f"Created default admin user: {admin.username}")
        else:
            print("Admin user already exists, skipping.")

        stats = ingest_all_docs(db)
        print(
            f"Document ingestion: {stats['created']} created, "
            f"{stats['updated']} updated, {stats['skipped']} skipped, {stats['chunks']} chunks"
        )
        if stats.get("embedding_failures"):
            print(f"Embedding failures (chunks stored without vectors): {stats['embedding_failures']}")
        if stats["errors"]:
            print(f"Errors: {stats['errors']}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
