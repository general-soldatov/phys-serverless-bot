from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

async def router(dp: Dispatcher):

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.reply(text='Hello, {name}'.format(name=message.from_user.first_name))