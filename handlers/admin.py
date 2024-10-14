from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Row, Button

from app.router import SLRouter
from app.keyboard.inline import UserQuestion
from app.config.config import TGbot, ADMIN, BUTTON

class Lecturer(StatesGroup):
    start = State()
    available = State()

async def handler_question(message: Message, widget: ManagedTextInput,
                       dialog_manager: DialogManager, text: str) -> None:
    dialog_manager.dialog_data['message_id'] = message.message_id
    await dialog_manager.next()

async def question_yes(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    user_id = dialog_manager.dialog_data['user_id']
    message_id = dialog_manager.dialog_data['message_id']
    await callback.bot.copy_message(chat_id=user_id, from_chat_id=TGbot.admin, message_id=message_id)
    await callback.message.edit_text(ADMIN['question_succesful'].format(user_id=user_id))
    await dialog_manager.done()

async def question_no(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

question_dialog = Dialog(
    Window(
        Const(ADMIN['reply_question']),
        TextInput(
            id='admin_input',
            on_success=handler_question
        ),
        state=Lecturer.start
    ),
    Window(
        Const(ADMIN['available_reply']),
        Row(
            Button(text=Const(BUTTON['yes']), id='yes', on_click=question_yes),
            Button(text=Const(BUTTON['no']), id='no', on_click=question_no)
        ),
        state=Lecturer.available
    )
)

router = SLRouter()

@router.callback_query(UserQuestion.filter())
async def send_question(callback: CallbackQuery, callback_data: UserQuestion, dialog_manager: DialogManager):
    await dialog_manager.start(state=Lecturer.start)
    dialog_manager.dialog_data['user_id'] = callback_data.user_id
    await callback.answer()