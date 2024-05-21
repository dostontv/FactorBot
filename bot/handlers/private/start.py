from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from bot.buttons.reply import menu
from db.models import User

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = await User().get(message.from_user.id)
    if not user:
        user = message.from_user.model_dump(include={"id", "username", "fullname"})
        await User().create(**user)
        await User().commit()
    await message.answer("Salom tanlang " + f"{hbold(message.from_user.full_name)}!", reply_markup=menu(),
                         parse_mode=ParseMode.HTML)
