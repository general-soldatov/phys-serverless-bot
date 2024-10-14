from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Row, Button

from .command import router
from app.config.config import TGbot, USER, BUTTON, COMMANDS


class Register(StatesGroup):
    start = State()
    available = State()

def user_check(text: str) -> str:
    if text == 'user':
        return text
    raise ValueError

async def correct_text(message: Message, widget: ManagedTextInput,
                       dialog_manager: DialogManager, text: str) -> None:
    if message.text == 'user':
        dialog_manager.dialog_data['name_user'] = {
            'name': 'user',
            'profile': 'HTTC',
            'group': '1-a'
            }
        await dialog_manager.next()


async def error_text(message: Message, widget: ManagedTextInput,
                     dialog_manager: DialogManager, error: ValueError):
    await message.answer(USER['uncorrect'])

async def success_register(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await callback.message.bot.send_message(chat_id=TGbot.admin,
                                            text=USER['register_admin'].format(**dialog_manager.dialog_data['name_user']))
    await callback.message.edit_text(USER['yes'].format(**dialog_manager.dialog_data['name_user']))
    await dialog_manager.done()

async def unsuccess_register(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def get_user(dialog_manager: DialogManager, **kwargs):
    return dialog_manager.dialog_data['name_user']

async def exit_user(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await callback.message.edit_text(USER['exit_reg'])
    await dialog_manager.reset_stack()

register_dialog = Dialog(
    Window(
        Const(COMMANDS['register']),
        TextInput(
            id='user_input',
            type_factory=user_check,
            on_success=correct_text,
            on_error=error_text
        ),
        Button(
            Const(BUTTON['exit']),
            id='exit',
            on_click=exit_user
        ),
        state=Register.start
    ),
    Window(
        Format(USER['available']),
        Row(
            Button(text=Const(BUTTON['yes']), id='yes', on_click=success_register),
            Button(text=Const(BUTTON['no']), id='no', on_click=unsuccess_register)
        ),
        getter=get_user,
        state=Register.available
    )
)

@router.message(Command('register'))
async def cmd_register(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=Register.start, mode=StartMode.RESET_STACK)