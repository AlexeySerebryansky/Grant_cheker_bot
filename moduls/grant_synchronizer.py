from moduls.parser.grant_object import Grant
from database.grant_repository import GrantRepository


class GrantSynchronizer:

    def __init__(self, repository: GrantRepository):
        self.repository = repository

    def sync(self, grants: list[Grant]) -> list[Grant]:

        db_grants = self.repository.get_active()

        db_keys = {
            (grant.source, grant.url)
            for grant in db_grants
        }

        current_active_keys = set()

        new_grants = []

        for grant in grants:
            key = (grant.source, grant.url)

            if self._is_active(grant):
                current_active_keys.add(key)

                if key not in db_keys:
                    self.repository.add_active(grant)
                    new_grants.append(grant)

            else:
                if key not in db_keys:
                    self.repository.add_archive(grant)

        # Active grants that disappeared from the source
        for db_grant in db_grants:
            key = (db_grant.source, db_grant.url)

            if key not in current_active_keys:
                self.repository.move_to_archive(db_grant)

        return new_grants


    @staticmethod
    def _is_active(grant: Grant) -> bool:
        return grant.status != "Прийом заявок завершено"