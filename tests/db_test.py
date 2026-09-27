from database.grant_repository import GrantRepository
from moduls.parser.grant_object import Grant


def test_database():

    repository = GrantRepository()

    grant = Grant(
        source="fundinghub",
        amount="100 000 грн",
        title="Test grant",
        description="Test description",
        tags=["IT", "Business"],
        company="Test company",
        deadline="31.12.2026",
        status="Нове",
        url="https://fundinghub.com.ua/grant/test-grant",
        full_description="Test description",
    )

    repository.add_active(grant)

    grants = repository.get_active()

    for grant in grants:
        print(
            grant.id,
            grant.source,
            grant.title,
            grant.url,
        )

if __name__ == "__main__":
    test_database()