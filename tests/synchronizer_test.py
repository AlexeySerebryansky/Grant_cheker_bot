from database.conection import SessionLocal
from database.grants_models import ActiveGrantDB, ArchiveGrantDB
from database.grant_repository import GrantRepository
from moduls.grant_synchronizer import GrantSynchronizer
from moduls.parser.grant_object import Grant


def make_grant(
    title: str,
    url: str,
    status: str = "Нове",
) -> Grant:
    return Grant(
        source="test",
        amount="100 000 грн",
        title=title,
        description=f"Description {title}",
        tags=["IT"],
        company="Test company",
        deadline="31.12.2026",
        status=status,
        url=url,
    )


def clear_database():
    with SessionLocal() as session:
        session.query(ActiveGrantDB).delete()
        session.query(ArchiveGrantDB).delete()
        session.commit()


def test_synchronizer():
    clear_database()

    repository = GrantRepository()
    synchronizer = GrantSynchronizer(repository)

    grant_a = make_grant(
        title="Grant A",
        url="https://test.com/grant-a",
    )

    grant_b = make_grant(
        title="Grant B",
        url="https://test.com/grant-b",
    )

    grant_c = make_grant(
        title="Grant C",
        url="https://test.com/grant-c",
    )

    # ---------------------------------------------------------
    # FIRST SYNC
    # ---------------------------------------------------------

    new_grants = synchronizer.sync([
        grant_a,
        grant_b,
    ])

    assert len(new_grants) == 2

    assert {
        grant.url
        for grant in new_grants
    } == {
        grant_a.url,
        grant_b.url,
    }

    active = repository.get_active()

    assert len(active) == 2

    assert {
        grant.url
        for grant in active
    } == {
        grant_a.url,
        grant_b.url,
    }

    print("FIRST SYNC: OK")

    # ---------------------------------------------------------
    # SECOND SYNC
    #
    # A remains active
    # B disappeared -> archive
    # C is new -> active
    # ---------------------------------------------------------

    new_grants = synchronizer.sync([
        grant_a,
        grant_c,
    ])

    assert len(new_grants) == 1
    assert new_grants[0].url == grant_c.url

    active = repository.get_active()

    assert {
        grant.url
        for grant in active
    } == {
        grant_a.url,
        grant_c.url,
    }

    with SessionLocal() as session:
        archive = session.query(ArchiveGrantDB).all()

        assert len(archive) == 1
        assert archive[0].url == grant_b.url

    print("SECOND SYNC: OK")

    # ---------------------------------------------------------
    # THIRD SYNC
    #
    # Same grants again.
    # Nothing should be considered new.
    # ---------------------------------------------------------

    new_grants = synchronizer.sync([
        grant_a,
        grant_c,
    ])

    assert new_grants == []

    active = repository.get_active()

    assert {
        grant.url
        for grant in active
    } == {
        grant_a.url,
        grant_c.url,
    }

    print("THIRD SYNC: OK")

    clear_database()

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    test_synchronizer()