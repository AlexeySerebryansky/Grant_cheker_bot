from sqlalchemy import select

from database.conection import SessionLocal
from database.client_models import UserDB, UsersProfileDB


class UserRepository:


    def get_by_chat_id(self, chat_id: int) -> UserDB | None:

        with SessionLocal() as session:
            return session.scalar(
                select(UserDB).where(
                    UserDB.chat_id == chat_id
                )
            )

    def create_user(self, chat_id: int) -> UserDB:

        with SessionLocal() as session:
            user = UserDB(
                chat_id=chat_id,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            return user

    def get_or_create_user(self, chat_id: int) -> UserDB:

        user = self.get_by_chat_id(chat_id)

        if user is not None:
            return user

        return self.create_user(chat_id)

    def create_profile(self, user_id: int, name: str, description: str,
                       embedding: str | None = None, ) -> UsersProfileDB:

        with SessionLocal() as session:
            profile = UsersProfileDB(
                user_id=user_id,
                name=name,
                description=description,
                embedding=embedding,
            )

            session.add(profile)
            session.commit()
            session.refresh(profile)

            return profile

    def get_profile(self, profile_id: int) -> UsersProfileDB | None:

        with SessionLocal() as session:
            return session.scalar(
                select(UsersProfileDB).where(
                    UsersProfileDB.id == profile_id
                )
            )

    def get_user_profiles(self, user_id: int) -> list[UsersProfileDB]:

        with SessionLocal() as session:
            result = session.scalars(
                select(UsersProfileDB)
                .where(
                    UsersProfileDB.user_id == user_id
                )
                .order_by(UsersProfileDB.id)
            ).all()

            return list(result)

    def get_active_profiles(self, user_id: int) -> list[UsersProfileDB]:

        with SessionLocal() as session:
            result = session.scalars(
                select(UsersProfileDB)
                .where(
                    UsersProfileDB.user_id == user_id,
                    UsersProfileDB.is_active.is_(True),
                )
                .order_by(UsersProfileDB.id)
            ).all()

            return list(result)

    def update_profile(self, profile_id: int, name: str, description: str, embedding: str | None = None) -> None:

        with SessionLocal() as session:
            profile = session.get(
                UsersProfileDB,
                profile_id,
            )

            if profile is None:
                return

            profile.name = name
            profile.description = description
            profile.embedding = embedding

            session.commit()

    def delete_profile(self, profile_id: int) -> None:

        with SessionLocal() as session:
            profile = session.get(
                UsersProfileDB,
                profile_id,
            )

            if profile is None:
                return

            session.delete(profile)
            session.commit()
