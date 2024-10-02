import asyncio
import json

from aiogram import Bot, Dispatcher
from aiogram.types import update
from load import dp, bot, register_handler

async def main():
    await register_handler(dp)
    await dp.start_polling(bot)

async def process_event(event, dp: Dispatcher, bot: Bot):
    """
    Converting an Yandex.Cloud functions event to an update and
    handling tha update.
    """
    up: dict = json.loads(event['body'])
    my_update = update.Update.model_validate(up, context={"bot": bot})
    await dp.feed_update(bot, my_update)

async def handler(event, context):
    """ Yandex.Cloud functions handler. """

    if event['httpMethod'] == 'POST':
        # Bot and dispatcher initialization
        await register_handler(dp)
        await process_event(event, dp, bot)
        return {'statusCode': 200, 'body': 'ok'}
    return {'statusCode': 405}


if __name__ == '__main__':
    """ Mount app`s enter in working mashine """
    asyncio.run(main())