from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from dynamodb_fsm import FSMDynamodb
# from dynamodb_fsm.database import Dynamodb
from dotenv import load_dotenv
from os import getenv

from handlers import command

load_dotenv()
TOKEN = getenv('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# storage = FSMDynamodb(with_destiny=True)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_routers(command.start_dialog, command.tech_dialog,
                   command.news_dialog, command.lang_dialog)
setup_dialogs(dp)

async def register_handler(dp: Dispatcher):
    await command.router(dp)
