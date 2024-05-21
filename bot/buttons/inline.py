from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import Category, Book, Order


async def books_category(orders_count=None):
    rkm = InlineKeyboardBuilder()
    categories: list[Category] = await Category().get_all()
    rkm.add(
        *[InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}") for category in categories])
    rkm.add(InlineKeyboardButton(text="🔍 Qidirsh", switch_inline_query_current_chat=''))
    if orders_count:
        rkm.add(InlineKeyboardButton(text=f"Korzinka ({orders_count})", callback_data="kor"))
    rkm.adjust(2, repeat=True)
    return rkm.as_markup()


async def category_books(c_id: int, orders_count=None):
    rkm = InlineKeyboardBuilder()
    books: list[Book] = (await Category().get(c_id)).books
    rkm.add(
        *[InlineKeyboardButton(text=book.title, callback_data=f"book_{book.id}_category_{c_id}") for book in books])
    rkm.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data=f"back_c"))
    rkm.adjust(2, repeat=True)
    return rkm.as_markup()


def book_btn(b_id, c_id, amount, count=1):
    rkm = InlineKeyboardBuilder()
    rkm.add(InlineKeyboardButton(text=" ➖ ", callback_data=f"minus_c_{c_id}_b_{b_id}_count_{count}_{amount}"))
    rkm.add(InlineKeyboardButton(text=f" {count} ", callback_data="count"))
    rkm.add(InlineKeyboardButton(text=" ➕ ", callback_data=f"plus_c_{c_id}_b_{b_id}_count_{count}_amount_{amount}"))
    rkm.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data=f"back_bc_{c_id}"))
    rkm.add(InlineKeyboardButton(text="🛒 Savatga qo'shish", callback_data=f"korzinka_c_{c_id}_b_{b_id}_co_{count}"))
    rkm.adjust(3, 2)
    return rkm.as_markup()
