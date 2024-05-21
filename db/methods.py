from sqlalchemy import select

from db import Order
from db.base import db


async def get_order_by_user_id(user_id, payment_status):
    query = select(Order).where(Order.user_id == user_id, Order.payment_status == payment_status)
    return (await db.execute(query)).scalars()
