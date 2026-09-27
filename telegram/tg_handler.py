from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.client_repository import UserRepository

from telegram.keyboards import (
    main_menu,
    profiles_keyboard,
    delete_confirmation_keyboard,
)
from telegram.states import ProfileState


router = Router()

user_repository = UserRepository()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id

    user = user_repository.get_or_create_user(chat_id)
    profiles = user_repository.get_active_profiles(user.id)

    await state.clear()

    if profiles:
        await message.answer(
            "Привіт! 👋\n\n"
            "Ти вже зареєстрований.\n"
            "Тут ти можеш керувати напрямами, "
            "за якими я буду шукати гранти.",
            reply_markup=main_menu(),
        )
        return

    await state.set_state(
        ProfileState.waiting_for_first_profile
    )

    await message.answer(
        "Привіт! 👋\n\n"
        "Розкажи трохи про себе та які гранти "
        "ти шукаєш.\n\n"
        "Наприклад:\n"
        "«Я займаюся сільським господарством, "
        "маю невелике фермерське господарство та "
        "шукаю гранти на придбання обладнання "
        "і розвиток бізнесу»."
    )


# =========================================================
# ADD PROFILE
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "profile:add"
)
async def add_profile_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(
        ProfileState.waiting_for_new_profile
    )

    await callback.message.answer(
        "Розкажи про новий напрям, "
        "за яким ти хочеш отримувати гранти."
    )


# =========================================================
# UPDATE PROFILE
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "profile:update"
)
async def update_profile_handler(callback: CallbackQuery):
    await callback.answer()

    chat_id = callback.message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        await callback.message.answer(
            "Спочатку натисни /start."
        )
        return

    profiles = user_repository.get_active_profiles(user.id)

    if not profiles:
        await callback.message.answer(
            "У тебе поки немає напрямів."
        )
        return

    await callback.message.answer(
        "Обери напрям, який хочеш оновити:",
        reply_markup=profiles_keyboard(
            "update",
            profiles,
        ),
    )


@router.callback_query(
    lambda callback: callback.data.startswith("profile:update:")
)
async def select_update_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    profile_id = int(
        callback.data.split(":")[-1]
    )

    chat_id = callback.message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        return

    profile = user_repository.get_profile(profile_id)

    if profile is None or profile.user_id != user.id:
        await callback.message.answer(
            "Цей напрям недоступний."
        )
        return

    await state.update_data(
        profile_id=profile_id
    )

    await state.set_state(
        ProfileState.waiting_for_update
    )

    await callback.message.answer(
        "Надішли нову інформацію про цей напрям.\n\n"
        "Я повністю заміню старий опис новим."
    )


# =========================================================
# DELETE PROFILE
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "profile:delete"
)
async def delete_profile_handler(callback: CallbackQuery):
    await callback.answer()

    chat_id = callback.message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        await callback.message.answer(
            "Спочатку натисни /start."
        )
        return

    profiles = user_repository.get_active_profiles(user.id)

    if not profiles:
        await callback.message.answer(
            "У тебе поки немає напрямів."
        )
        return

    await callback.message.answer(
        "Обери напрям, який хочеш видалити:",
        reply_markup=profiles_keyboard(
            "delete",
            profiles,
        ),
    )


@router.callback_query(
    lambda callback: callback.data.startswith("profile:delete:")
)
async def select_delete_profile(callback: CallbackQuery):
    await callback.answer()

    profile_id = int(
        callback.data.split(":")[-1]
    )

    chat_id = callback.message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        return

    profile = user_repository.get_profile(profile_id)

    if profile is None or profile.user_id != user.id:
        await callback.message.answer(
            "Цей напрям недоступний."
        )
        return

    await callback.message.answer(
        f"Точно видалити напрям:\n\n"
        f"<b>{profile.name}</b>\n\n"
        f"{profile.description}",
        reply_markup=delete_confirmation_keyboard(
            profile.id
        ),
        parse_mode="HTML",
    )


@router.callback_query(
    lambda callback: callback.data.startswith(
        "profile:delete_confirm:"
    )
)
async def confirm_delete_profile(callback: CallbackQuery):
    await callback.answer()

    profile_id = int(
        callback.data.split(":")[-1]
    )

    chat_id = callback.message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        return

    profile = user_repository.get_profile(profile_id)

    if profile is None or profile.user_id != user.id:
        await callback.message.answer(
            "Цей напрям недоступний."
        )
        return

    user_repository.delete_profile(profile_id)

    await callback.message.answer(
        "🗑 Напрям видалено.",
        reply_markup=main_menu(),
    )

# =========================================================
# LIST PROFILES
# =========================================================

    @router.callback_query(
        lambda callback: callback.data == "profile:list"
    )
    async def list_profiles_handler(callback: CallbackQuery):
        await callback.answer()

        chat_id = callback.message.chat.id
        user = user_repository.get_by_chat_id(chat_id)

        if user is None:
            await callback.message.answer(
                "Спочатку натисни /start."
            )
            return

        profiles = user_repository.get_active_profiles(user.id)

        if not profiles:
            await callback.message.answer(
                "У тебе поки немає збережених напрямів.",
                reply_markup=main_menu(),
            )
            return

        lines = ["👤 <b>Твої напрями:</b>", ""]

        for index, profile in enumerate(profiles, start=1):
            lines.append(
                f"<b>{index}. {profile.name}</b>"
            )
            lines.append(profile.description)
            lines.append("")

        await callback.message.answer(
            "\n".join(lines),
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


# =========================================================
# BACK
# =========================================================

@router.callback_query(
    lambda callback: callback.data == "profile:back"
)
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await callback.message.answer(
        "Головне меню:",
        reply_markup=main_menu(),
    )


# =========================================================
# TEXT / PROFILE CREATION / UPDATE
# =========================================================

@router.message(ProfileState.waiting_for_first_profile)
async def first_profile_handler(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(
            "Будь ласка, надішли інформацію текстом."
        )
        return

    chat_id = message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        await message.answer(
            "Спочатку натисни /start."
        )
        return

    user_repository.create_profile(
        user_id=user.id,
        name="Новий напрям",
        description=message.text,
    )

    await state.clear()

    await message.answer(
        "Дякую! 👍\n\n"
        "Я зберіг інформацію про тебе.\n"
        "Тепер просто чекай повідомлення, "
        "коли знайду відповідні гранти.",
        reply_markup=main_menu(),
    )


@router.message(ProfileState.waiting_for_new_profile)
async def new_profile_handler(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(
            "Будь ласка, надішли інформацію текстом."
        )
        return

    chat_id = message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        await message.answer(
            "Спочатку натисни /start."
        )
        return

    user_repository.create_profile(
        user_id=user.id,
        name="Новий напрям",
        description=message.text,
    )

    await state.clear()

    await message.answer(
        "✅ Новий напрям додано.",
        reply_markup=main_menu(),
    )


@router.message(ProfileState.waiting_for_update)
async def update_profile_text_handler(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(
            "Будь ласка, надішли інформацію текстом."
        )
        return

    data = await state.get_data()
    profile_id = data.get("profile_id")

    if profile_id is None:
        await state.clear()
        await message.answer(
            "Не вдалося визначити напрям. "
            "Спробуй ще раз."
        )
        return

    chat_id = message.chat.id
    user = user_repository.get_by_chat_id(chat_id)

    if user is None:
        await state.clear()
        return

    profile = user_repository.get_profile(profile_id)

    if profile is None or profile.user_id != user.id:
        await state.clear()
        await message.answer(
            "Цей напрям недоступний."
        )
        return

    user_repository.update_profile(
        profile_id=profile.id,
        name=profile.name,
        description=message.text,
        embedding=None,
    )

    await state.clear()

    await message.answer(
        "✅ Інформацію про напрям оновлено.",
        reply_markup=main_menu(),
    )