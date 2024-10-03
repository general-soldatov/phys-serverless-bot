from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from dynamodb_fsm import FSMDynamodb
from dotenv import load_dotenv
from os import getenv

from handlers import command

load_dotenv()
TOKEN = getenv('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# storage = FSMDynamodb()
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(command.start_dialog)
setup_dialogs(dp)

async def register_handler(dp: Dispatcher):
    await command.router(dp)
