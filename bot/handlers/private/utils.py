from config import conf
from db.models import Book


async def book_make_detail(book_id: int):
    book: Book = await Book.get(book_id)
    caption = """
    {title}: {book_title}
{author}: {book_author}
{genre}: {book_category_name} 
{page}: {book_page}
{about}: {book_description}
{price}: {book_price} {book_money_type_value}
    """.format(
        title="🔹 Nomi",
        book_title=book.title,
        author="✍🏻Mualif",
        book_author=book.author,
        genre="🟤 Janri",
        book_category_name=book.category.name,
        page="📑 Bet",
        book_page=book.page,
        about="📖 Kitob haqida",
        book_description=book.description,
        price="💸 Narxi",
        book_price=book.price,
        book_money_type_value=book.money_type.value
    )
    photo = f"https://t.me/{conf.bot.CHANNEL_ID[1:]}/{book.photo.message_id}"
    return caption, photo, book.amount
