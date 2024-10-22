import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from app.config.config import TGbot, USER, ADMIN
from app.connect.db_user import DBUser


logger = logging.getLogger(__name__)

class StudentsMessageMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user: User = data.get('event_from_user')
        try:
            data_user = DBUser().info_user(user.id)
            if data_user['active'] > 1:
                result = await handler(event, data)
            else:
                result = await event.bot.send_message(chat_id=user.id, text=USER['permission_denied'])

        except Exception as e:
            errors = f'Errors from {user.id} "{user.first_name} {user.last_name}": {e}'
            result = await event.bot.send_message(chat_id=int(TGbot.admin),
                                                  text=ADMIN['errors_middleware'].format(errors=errors))
        return result

class FirstOuterMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user: User = data.get('event_from_user')
        try:
            data_user = DBUser().info_user(user.id)
            if data_user['active'] != 0:
                result = await handler(event, data)
            else:
                result = await event.bot.send_message(chat_id=user.id, text=USER['permission_denied'])

        except IndexError:
            name_user = f'{user.first_name} {user.last_name}'
            DBUser().put_item(user.id, name_user)
            logger.error('Index Error')
            result = await handler(event, data)
        except Exception as e:
            errors = f'Errors from {user.id} "{user.first_name} {user.last_name}": {e}'
            result = await event.bot.send_message(chat_id=int(TGbot.admin),
                                                  text=ADMIN['errors_middleware'].format(errors=errors))

        return result