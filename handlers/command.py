from aiogram import Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, User
from aiogram.filters import CommandStart, Command

from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

class StartStorage(StatesGroup):
    start = State()

async def yes_click_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await callback.message.edit_text('<b>Succesful</b> This is wonderfull!')
    await dialog_manager.done()

async def no_click_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await callback.message.edit_text('<b>Unuccesful</b> I`m lied!')
    await dialog_manager.done()

async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'username': event_from_user.username}

start_dialog = Dialog(
    Window(
        Format('Hello, {username}! \n'),
        Const('Can yoy make chat-bot with aiogram?'),
        Row(
            Button(text=Const('[^] Yes'), id='yes', on_click=yes_click_handler),
            Button(text=Const('[?] No'), id='no', on_click=no_click_handler)
        ),
        getter=user_getter,
        state=StartStorage.start
    ),
)

async def router(dp: Dispatcher):

    @dp.message(CommandStart())
    async def start(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(state=StartStorage.start, mode=StartMode.RESET_STACK)