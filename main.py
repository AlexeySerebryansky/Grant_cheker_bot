from dotenv import load_dotenv

load_dotenv()

import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from client.client import Client
from moduls.parser.funding_hub import FundingHub
from database.grant_repository import GrantRepository
from moduls.grant_synchronizer import GrantSynchronizer

from telegram.tg_handler import router

load_dotenv()


async def grant_check():
    print("=== GRANT CHECK START ===")

    client = Client()
    await client.start()
    parser = FundingHub()

    repository = GrantRepository()
    synchronizer = GrantSynchronizer(repository)

    try:
        print("Getting HTML...")

        html = await client.get_html(
            "https://fundinghub.com.ua/grants"
        )

        print(f"HTML received: {len(html)} characters")

        grants = parser.parse(html)

        print(f"Grants parsed: {len(grants)}")

        for i, grant in enumerate(grants, start=1):
            print(f"[{i}/{len(grants)}] Getting {grant.url}")

            detail_html = await client.get_html(grant.url)

            grant.full_description = parser.parse_detail(
                detail_html
            )

        new_grants = synchronizer.sync(grants)

        print(f"New grants: {len(new_grants)}")

        print("=== GRANT CHECK FINISHED ===")

    finally:
        await client.close()


async def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is not set")

    bot = Bot(token=token)

    dp = Dispatcher()
    dp.include_router(router)

    try:
        await asyncio.gather(
            dp.start_polling(bot),
        )

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(grant_check())

