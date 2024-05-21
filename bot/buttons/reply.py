from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def menu():
    rkm = ReplyKeyboardBuilder()
    rkm.add(*[
        KeyboardButton(text="📚 Kitoblar"),
        KeyboardButton(text="🛍 Buyurtmalarim"),
        KeyboardButton(text="🌐 Mening buyurtmalarim"),
        KeyboardButton(text="📞 Biz bilan bog'lanish"),
    ])
    rkm.adjust(1, 1, 2)
    return rkm.as_markup(resize_keyboard=True)
