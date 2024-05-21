from sqlalchemy import BIGINT
from sqlalchemy import ForeignKey, SMALLINT, TEXT, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import CreatedModel, AbstractClass, Base
from db.utils import CustomImageField
from enums import MoneyType, LangType, StatusEnum


class User(CreatedModel):
    id: Mapped[int] = mapped_column(__type_pos=BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    fullname: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    lang: Mapped[str] = mapped_column(Enum(LangType, values_callable=lambda m: [field.value for field in m]),
                                      server_default=LangType.EN.value)
    categories: Mapped[list['Category']] = relationship("Category", back_populates="owner", lazy="selectin")
    orders: Mapped[list['Order']] = relationship("Order", back_populates="user", lazy="selectin")


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column("owner_id", BIGINT, ForeignKey("users.id", ondelete="SET NULL"),
                                          nullable=True)
    owner: Mapped['User'] = relationship("User", back_populates="categories", lazy="selectin")
    books: Mapped[list['Book']] = relationship("Book", back_populates="category", lazy="selectin")


class Book(CreatedModel):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=True)
    page: Mapped[str] = mapped_column(__type_pos=SMALLINT, nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(TEXT)
    amount: Mapped[str] = mapped_column(__type_pos=SMALLINT)
    photo: Mapped[str] = mapped_column(CustomImageField)
    money_type: Mapped[str] = mapped_column(Enum(MoneyType, values_callable=lambda m: [field.value for field in m]),
                                            server_default=MoneyType.UZS.value)
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id", ondelete="CASCADE"))
    category: Mapped['Category'] = relationship("Category", back_populates="books", lazy="selectin")


class Order(CreatedModel):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(Enum(StatusEnum, values_callable=lambda m: [field.value for field in m]),
                                        server_default=StatusEnum.PENDING.value)
    payment_status: Mapped[str] = mapped_column(
        Enum(StatusEnum, values_callable=lambda m: [field.value for field in m]),
        server_default=StatusEnum.PENDING.value)
    user_id: Mapped[int] = mapped_column('user_id', BIGINT, ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped['User'] = relationship("User", back_populates="orders", lazy="selectin")
    order_items: Mapped[list['OrderItem']] = relationship("OrderItem", back_populates='order', lazy="selectin")


class OrderItem(AbstractClass, Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    count: Mapped[int] = mapped_column(server_default="1")
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    order: Mapped['Order'] = relationship("Order", back_populates='order_items')
