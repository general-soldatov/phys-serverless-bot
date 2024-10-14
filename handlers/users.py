from aiogram import F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from app.router import SLRouter
from app.config.config import COMMANDS, USER, BUTTON
from app.keyboard.reply import ReplyButton
from app.keyboard.inline import UserInline

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

@router.message(Command('contact'))
async def cmd_contacts(message: Message):
    builder = UserInline(width=2).contact()
    await message.answer(COMMANDS['contact'], reply_markup=builder)
    await message.delete()

@router.message(Command('menu'))
async def cmd_menu(message: Message):
    buttons = ReplyButton(width=3)(user_id=message.from_user.id)
    await message.answer(text=COMMANDS['menu'], reply_markup=buttons)
    await message.delete()

@router.message(Command('cancel'), StateFilter(default_state))
async def cmd_cancel(message: Message):
    await message.answer(text=COMMANDS['cancel_not'])

@router.message(Command('cancel'), ~StateFilter(default_state))
async def cmd_cancel_state(message: Message, state: FSMContext):
    await message.answer(text=COMMANDS['cancel'])
    await state.clear()

@router.message(F.text == BUTTON['metodic'])
async def button_metodic(message: Message):
    builder = UserInline(width=2).metodic()
    await message.answer(USER['metodic'], reply_markup=builder)
    await message.delete()

@router.message(F.text == BUTTON['textbook'])
async def button_book(message: Message):
    builder = UserInline().textbook()
    await message.answer(USER['textbook'], reply_markup=builder)
    await message.delete()