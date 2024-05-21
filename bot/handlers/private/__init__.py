from aiogram import Router
from aiogram.enums import ChatType

from bot.filters.chat_type_filter import ChatTypeFilter
from bot.handlers.private.book import book_router
from bot.handlers.private.start import start_router

private_router = Router()

private_router.message.filter(ChatTypeFilter(ChatType.PRIVATE))

private_router.include_routers(start_router, book_router)
