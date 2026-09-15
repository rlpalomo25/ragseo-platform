import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.services.doc_ingestion import ingest_all_docs


def main():
    db = SessionLocal()
    try:
        stats = ingest_all_docs(db)
        print(f"Created: {stats['created']}")
        print(f"Updated: {stats['updated']}")
        print(f"Skipped: {stats['skipped']}")
        if stats["errors"]:
            print(f"Errors: {len(stats['errors'])}")
            for err in stats["errors"]:
                print(f"  - {err}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
