from sqlalchemy import BigInteger, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from database.base import Base


class GrantDBBase:
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    source: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    amount: Mapped[str | None] = mapped_column(Text)

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(Text)

    tags: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text)
    )

    company: Mapped[str | None] = mapped_column(Text)

    deadline: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str | None] = mapped_column(Text)

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    full_description: Mapped[str | None] = mapped_column(Text)

    embedding: Mapped[str | None] = mapped_column(
        Vector(1024)
    )


class ActiveGrantDB(GrantDBBase, Base):
    __tablename__ = "active_grants"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "url",
            name="uq_active_grant_source_url"
        ),
    )


class ArchiveGrantDB(GrantDBBase, Base):
    __tablename__ = "archive_grants"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "url",
            name="uq_archive_grant_source_url"
        ),
    )