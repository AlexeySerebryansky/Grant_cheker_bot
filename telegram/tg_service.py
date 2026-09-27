import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()


class TelegramService:
    MAX_MESSAGE_LENGTH = 4000

    def __init__(self):
        token = os.getenv("BOT_TOKEN")

        if not token:
            raise ValueError("BOT_TOKEN is not set")

        self.bot = Bot(token=token)

    async def send_message(self, chat_id: int, text: str) -> None:
        messages = self._split_message(text)

        for message in messages:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="HTML",
            )

    def _split_message(self, text: str) -> list[str]:
        if len(text) <= self.MAX_MESSAGE_LENGTH:
            return [text]

        messages = []
        remaining = text

        while len(remaining) > self.MAX_MESSAGE_LENGTH:
            split_at = remaining.rfind(
                "\n",
                0,
                self.MAX_MESSAGE_LENGTH
            )

            if split_at == -1:
                split_at = remaining.rfind(
                    " ",
                    0,
                    self.MAX_MESSAGE_LENGTH
                )

            if split_at == -1:
                split_at = self.MAX_MESSAGE_LENGTH

            messages.append(
                remaining[:split_at].strip()
            )

            remaining = remaining[split_at:].strip()

        if remaining:
            messages.append(remaining)

        return messages

    async def close(self) -> None:
        await self.bot.session.close()
