from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs
from dataclasses import dataclass
from dynamodb_fsm import FSMDynamodb
# from dynamodb_fsm.database import Dynamodb
from dotenv import load_dotenv
from os import getenv

from app.config.config import TGbot
from handlers import command, register, question, task
from app.router import SLDispatcher

load_dotenv()
@dataclass
class DatabaseConfig:
    endpoint_url: str = getenv('ENDPOINT')
    region_name: str = getenv('REGION_NAME')
    aws_access_key_id: str = getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = getenv('AWS_SECRET_ACCESS_KEY')


config = DatabaseConfig().__dict__

TOKEN = TGbot().token
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# storage = FSMDynamodb(with_destiny=True, config=config)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
# comand`s dialog router
dp.include_routers(task.dp, question.dp, command.router)
dp.include_routers(command.start_dialog, command.tech_dialog,
                   command.news_dialog, command.lang_dialog)
# user register
dp.include_routers(register.register_dialog, question.question,
                   question.shedule_dialog, task.task_dialog)
setup_dialogs(dp)

# async def register_handler(dp: Dispatcher):
#     await register.router(dp)
    # await question.router(dp)
    # await task.router(dp)
