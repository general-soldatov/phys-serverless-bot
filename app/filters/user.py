from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union

from app.config.config import BUTTON


class UserReply(BaseFilter):
    """Фильтр на кнопки reply-markdown кнопки
    """
    def __init__(self, name_button: Union[str, list]) -> None:
        self.name_button = name_button

    async def __call__(self, message: Message) -> Any:
        if isinstance(self.name_button, str):
            return message.text == BUTTON[self.name_button]
        return message.text in [BUTTON[i] for i in self.name_button]