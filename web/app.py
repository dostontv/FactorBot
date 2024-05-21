import os

import uvicorn
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from config import conf
from db import User, Book, Category, database, Order, OrderItem
from web.provider import UsernameAndPasswordProvider

middleware = [
    Middleware(SessionMiddleware, secret_key=conf.web.SECRET_KEY)
]

app = Starlette(middleware=middleware)

admin = Admin(
    engine=database._engine,
    title="Aiogram Web Admin",
    base_url='/',
    logo_url="https://telegra.ph/file/8e3f4e8667739be796287.png",
    auth_provider=UsernameAndPasswordProvider()
)


class DelModelView(ModelView):
    exclude_fields_from_list = ('created_at', 'updated_at')
    exclude_fields_from_create = ('created_at', 'updated_at')
    exclude_fields_from_edit = ('created_at', 'updated_at')


admin.add_view(DelModelView(User))
admin.add_view(DelModelView(Category))
admin.add_view(DelModelView(Book))
admin.add_view(DelModelView(Order))
admin.add_view(ModelView(OrderItem))

admin.mount_to(app)

os.makedirs("./media/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
StorageManager.add_storage("default", container)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
