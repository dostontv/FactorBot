from typing import Any, List, Dict, Union

import requests
from sqlalchemy.engine import Dialect
from sqlalchemy_file import ImageField

from config import conf


def upload_photo(photo) -> int:
    url = f"https://api.telegram.org/bot{conf.bot.BOT_TOKEN}/sendPhoto?chat_id={conf.bot.CHANNEL_ID}&caption=Yangi%20kitob%20qo%27shildi"
    m_id = requests.post(url, files={'photo': photo}).json()

    return m_id["result"]["message_id"]


class CustomImageField(ImageField):
    def process_bind_param(self, value: Any, dialect: Dialect) -> Union[None, Dict[str, Any], List[Dict[str, Any]]]:
        if value:
            m_id = upload_photo(value.file)
            data = {
                'message_id': m_id
            }
            value.update(data)
        return super().process_bind_param(value, dialect)
