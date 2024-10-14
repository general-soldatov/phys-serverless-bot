from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from app.router import SLRouter
from app.config.config import COMMANDS
from app.keyboard.reply import ReplyButton

router = SLRouter()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # register = UserUn()
    # register.put_item(user_id=message.from_user.id, name=message.from_user.first_name)
    # buttons = UserButton().unauth_user()
    await message.reply(text=COMMANDS['start'].format(name=message.from_user.first_name),)
                        # reply_markup=buttons)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(text=COMMANDS['help'])

@router.message(Command(commands=['menu']))
async def cmd_menu(message: Message):
    buttons = ReplyButton(width=3)(user_id=message.from_user.id)
    await message.answer(text=COMMANDS['menu'], reply_markup=buttons)

@router.message(Command(commands=['cancel']), StateFilter(default_state))
async def cmd_cancel(message: Message):
    await message.answer(text=COMMANDS['cancel_not'])

@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def cmd_cancel_state(message: Message, state: FSMContext):
    await message.answer(text=COMMANDS['cancel'])
    await state.clear()