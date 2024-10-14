from aiogram.filters import Command
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog import Dialog, DialogManager, Window, StartMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from app.config.config import TGbot, USER, BUTTON
from app.api.user_api import Shedule
from app.router import SLRouter
from app.keyboard.inline import AdminInline

class Question(StatesGroup):
    start = State()

class SheduleState(StatesGroup):
    window_today = State()
    window_tomorrow = State()
    window_after_tom = State()
    window_to_2_day = State()

async def message_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    buttons = AdminInline(width=1).question(message.from_user.id)
    data_question = dict(user_id=message.from_user.id, name='Yurs', profile='HTTC', group='1-a')
    await message.bot.send_message(chat_id=TGbot.admin,
                                   text=USER['send_question'].format(**data_question), reply_markup=buttons)
    await message.bot.copy_message(chat_id=TGbot().admin, from_chat_id=str(message.from_user.id),
                                   message_id=message.message_id)
    await message.answer(text=USER['get_question'])
    await dialog_manager.done()

question = Dialog(
    Window(
        Const(text=USER['question']),
        MessageInput(
            func=message_handler,
            content_types=ContentType.ANY
        ),
        state=Question.start,

    )
)

lst_window = [
    Window(
        Const(item['text']),
        Row(
            *[SwitchTo(Const(BUTTON[data]), id=data,
                       state=SheduleState.__dict__[f"window_{data}"]) for data in item['id']]
        ),
        state=SheduleState.__dict__[f"window_{item['day']}"]
    )
for item in Shedule().data()]

shedule_dialog = Dialog(*lst_window)

router = SLRouter()

@router.message(Command('question'))
async def question_cmd(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=Question.start, mode=StartMode.RESET_STACK)

@router.message(Command('shedule'))
async def shedule(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SheduleState.window_today, mode=StartMode.RESET_STACK)
