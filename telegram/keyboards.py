from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 Мої профілі",
                    callback_data="profile:list",
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Додати напрям",
                    callback_data="profile:add",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Оновити напрям",
                    callback_data="profile:update",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Видалити напрям",
                    callback_data="profile:delete",
                )
            ],
        ]
    )


def profiles_keyboard(action: str, profiles) -> InlineKeyboardMarkup:
    buttons = []

    for profile in profiles:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"#{profile.id} {profile.name}",
                    callback_data=f"profile:{action}:{profile.id}",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="profile:back",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def delete_confirmation_keyboard(profile_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 Так, видалити",
                    callback_data=f"profile:delete_confirm:{profile_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="profile:back",
                )
            ],
        ]
    )