import csv
import json
from pathlib import Path

from sqlalchemy import select

from database.conection import SessionLocal
from database.grants_models import ActiveGrantDB, ArchiveGrantDB

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_FILE = BASE_DIR / "grants.csv"


COLUMNS = [
    "id",
    "source",
    "amount",
    "title",
    "description",
    "full_description",
    "tags",
    "company",
    "deadline",
    "status",
    "url",
    "is_active"
]


def export_grants() -> None:
    with SessionLocal() as session:
        active_grants = session.scalars(
            select(ActiveGrantDB)
        ).all()

        archive_grants = session.scalars(
            select(ArchiveGrantDB)
        ).all()

    grants = []

    for grant in active_grants:
        grants.append({
            "id": grant.id,
            "source": grant.source,
            "amount": grant.amount,
            "title": grant.title,
            "description": grant.description,
            "full_description": grant.full_description,
            "tags": json.dumps(grant.tags or [], ensure_ascii=False),
            "company": grant.company,
            "deadline": grant.deadline,
            "status": grant.status,
            "url": grant.url,
            "is_active": True
        })

    for grant in archive_grants:
        grants.append({
            "id": grant.id,
            "source": grant.source,
            "amount": grant.amount,
            "title": grant.title,
            "description": grant.description,
            "full_description": grant.full_description,
            "tags": json.dumps(grant.tags or [], ensure_ascii=False),
            "company": grant.company,
            "deadline": grant.deadline,
            "status": grant.status,
            "url": grant.url,
            "is_active": False
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS
        )

        writer.writeheader()
        writer.writerows(grants)

    print(f"Active grants: {len(active_grants)}")
    print(f"Archived grants: {len(archive_grants)}")
    print(f"Total grants: {len(grants)}")
    print(f"CSV saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    export_grants()