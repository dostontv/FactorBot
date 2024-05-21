from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.buttons.inline import books_category, category_books, book_btn
from bot.handlers.private.utils import book_make_detail
from db import Order, OrderItem
from db.methods import get_order_by_user_id
from enums import StatusEnum

book_router = Router()


@book_router.message(F.text == "📚 Kitoblar")
async def start_book(message: Message):
    await message.answer("Kategoriyalardan birini tanlang", reply_markup=await books_category())


@book_router.callback_query(F.data.startswith("category_"))
async def category_book(call: CallbackQuery):
    data = int(call.data.split("category_")[1])
    await call.message.edit_text("Kitoblardan birini tanlang", reply_markup=await category_books(data))


@book_router.callback_query(F.data.startswith("book_"))
async def book(call: CallbackQuery):
    await call.message.delete()
    data = call.data.split("_")
    book_id = int(data[1])
    txt, photo, amount = await book_make_detail(book_id)
    await call.message.answer_photo(photo, txt, reply_markup=book_btn(book_id, data[3], amount))


@book_router.callback_query(F.data.startswith("back_"))
async def back_book(call: CallbackQuery):
    data = call.data.split("_")
    if data[1] == "bc":
        await call.message.delete()
        await call.message.answer("Kitoblardan birini tanlang",
                                  reply_markup=await category_books(int(data[-1])))
    else:
        await call.message.edit_text("Kategoriyalardan birini tanlang", reply_markup=await books_category())


@book_router.callback_query(F.data.startswith("minus_"))
async def minus_b_book_handler(call: CallbackQuery):
    data = call.data.split('_')
    if int(data[6]) > 1:
        await call.message.edit_reply_markup(reply_markup=book_btn(data[4], data[2], data[-1], int(data[6]) - 1))
    else:
        await call.answer(text="1 ta buyurtma bera olasiz", show_alert=True)


@book_router.callback_query(F.data.startswith("plus_"))
async def plus_b_book_handler(call: CallbackQuery):
    data = call.data.split('_')
    if int(data[-3]) < int(data[-1]):
        await call.message.edit_reply_markup(reply_markup=book_btn(data[4], data[2], data[-1], int(data[6]) + 1))
    else:
        await call.answer(text="Siz {ta} ta buyurtma bera olasiz".format(ta=data[-1]), show_alert=True)


@book_router.callback_query(F.data.startswith("korzinka_"))
async def create_order_handler(call: CallbackQuery):
    # TODO
    call_data = call.data.split('_')
    order = await get_order_by_user_id(call.from_user.id, StatusEnum.PENDING.value)
    l = len(order)
    if l == 0:
        data = {
            "status": StatusEnum.PENDING.value,
            "payment_status": StatusEnum.PENDING.value,
            "user_id": call.from_user.id,
        }
        order_id = await Order.create(**data)
    # await OrderItem.create(**{"count": int(call_data[-1]),"order_id":})
    await call.message.edit_text("Kitoblardan birini tanlang",
                                 reply_markup=await category_books(int(call_data[2]), l))
