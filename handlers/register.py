from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.text import Const

class Register(StatesGroup):
    start = State()

def user_check(text: str) -> str:
    if text == 'user':
        return text
    raise ValueError

async def correct_text(message: Message, widget: ManagedTextInput,
                       dialog_manager: DialogManager, text: str) -> None:
    await message.answer(text=f'You are {text}')

async def error_text(message: Message, widget: ManagedTextInput,
                     dialog_manager: DialogManager, error: ValueError):
    await message.answer('Uncorrect data')

register_dialog = Dialog(
    Window(
        Const(text='Insert you name:'),
        TextInput(
            id='user_input',
            type_factory=user_check,
            on_success=correct_text,
            on_error=error_text
        ),
        state=Register.start
    )
)

async def router(dp: Dispatcher):

    @dp.message(Command('register'))
    async def start(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(state=Register.start)