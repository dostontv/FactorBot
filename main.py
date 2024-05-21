import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.handlers import private_router
from config import conf
from db import database

i18n = I18n(path="locales")
dp = Dispatcher()


async def on_startup() -> None:
    await database.create_all()

    dp.include_routers(*[private_router])


async def main() -> None:
    dp.startup.register(on_startup)
    # dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    bot = Bot(conf.bot.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
