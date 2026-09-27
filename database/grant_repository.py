from sqlalchemy import select

from database.conection import SessionLocal
from database.grants_models import ActiveGrantDB, ArchiveGrantDB
from moduls.parser.grant_object import Grant


class GrantRepository:

    def add_active(self, grant: Grant) -> None:
        with SessionLocal() as session:
            db_grant = ActiveGrantDB(
                source=grant.source,
                amount=grant.amount,
                title=grant.title,
                description=grant.description,
                full_description=grant.full_description,
                tags=grant.tags,
                company=grant.company,
                deadline=grant.deadline,
                status=grant.status,
                url=grant.url
            )

            session.add(db_grant)
            session.commit()

    def get_active(self) -> list[ActiveGrantDB]:
        with SessionLocal() as session:
            result = session.scalars(
                select(ActiveGrantDB)
            ).all()

            return list(result)

    def get_active_by_key(self, source: str, url: str) -> ActiveGrantDB | None:

        with SessionLocal() as session:
            return session.scalar(
                select(ActiveGrantDB).where(
                    ActiveGrantDB.source == source,
                    ActiveGrantDB.url == url,
                )
            )

    def add_archive(self, grant: Grant) -> None:
        with SessionLocal() as session:
            db_grant = ArchiveGrantDB(
                source=grant.source,
                amount=grant.amount,
                title=grant.title,
                description=grant.description,
                full_description=grant.full_description,
                tags=grant.tags,
                company=grant.company,
                deadline=grant.deadline,
                status=grant.status,
                url=grant.url
            )

            session.add(db_grant)
            session.commit()

    def move_to_archive(self, grant: ActiveGrantDB) -> None:
        with SessionLocal() as session:
            archive_grant = ArchiveGrantDB(
                source=grant.source,
                amount=grant.amount,
                title=grant.title,
                description=grant.description,
                full_description=grant.full_description,
                tags=grant.tags,
                company=grant.company,
                deadline=grant.deadline,
                status=grant.status,
                url=grant.url,
            )

            session.add(archive_grant)

            active_grant = session.get(
                ActiveGrantDB,
                grant.id
            )

            if active_grant:
                session.delete(active_grant)

            session.commit()

    def update_full_description(self, grant: Grant) -> None:
        with SessionLocal() as session:
            db_grant = session.scalar(
                select(ActiveGrantDB).where(
                    ActiveGrantDB.source == grant.source,
                    ActiveGrantDB.url == grant.url,
                )
            )

            if db_grant is None:
                return

            db_grant.full_description = grant.full_description

            session.commit()