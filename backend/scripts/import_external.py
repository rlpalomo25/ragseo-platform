import sys
import os
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import get_settings
from app.database import SessionLocal
from app.services.external_ingest import import_external_folder
from app.services.learning_loop import snapshot_publications


def main():
    parser = argparse.ArgumentParser(description="Import weekly external market-data exports")
    parser.add_argument("--path", help="Override external data folder (default: settings.external_data_path)")
    parser.add_argument("--force", action="store_true", help="Re-import files whose hash is already stored")
    args = parser.parse_args()

    data_dir = Path(args.path) if args.path else Path(get_settings().external_data_path)
    db = SessionLocal()
    try:
        results = import_external_folder(data_dir, db, force=args.force)
        for r in results:
            status = r["status"]
            suffix = {"imported": f" ({r['rows']} rows)",
                      "skipped": " (already imported)"}.get(status, "")
            err = f" - {r['error']}" if r.get("error") else ""
            print(f"[{status.upper()}] {r['filename']}{suffix}{err}")
        by_status = {}
        for r in results:
            by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        print(f"\nTotal: {len(results)} files -> " +
              ", ".join(f"{k}: {v}" for k, v in sorted(by_status.items())))
        learning = snapshot_publications(db)
        print(
            f"Learning loop: {learning.get('snapshots', 0)} snapshots, "
            f"{learning.get('signals', 0)} signals"
        )
        if by_status.get("error"):
            sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()