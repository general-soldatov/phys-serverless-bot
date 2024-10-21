import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from app.config.config import TGbot, USER


logger = logging.getLogger(__name__)

class AdminMessageMiddleware(BaseMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user: User = data.get('event_from_user')
        if user.id == int(TGbot.admin):
            result = await handler(event, data)
        else:
            result = await event.bot.send_message(chat_id=user.id, text=USER['permission_denied'])
        return result