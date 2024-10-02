from aiogram import Bot, Dispatcher
from dynamodb_fsm import FSMDynamodb
from dotenv import load_dotenv
from os import getenv

from handlers import command

load_dotenv()
TOKEN = getenv('TOKEN')
bot = Bot(token=TOKEN)
storage = FSMDynamodb()
dp = Dispatcher(storage=storage)

async def register_handler(dp: Dispatcher):
    await command.router(dp)
