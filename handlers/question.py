from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.enums import ContentType, ParseMode
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Next, Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from app.config.config import TGbot
from app.api.user_api import Shedule

class Question(StatesGroup):
    start = State()
    cancel = State()

class SheduleState(StatesGroup):
    window_today = State()
    window_tomorrow = State()
    window_after_tom = State()
    window_to_2_day = State()

async def message_handler(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    await message.bot.copy_message(chat_id=TGbot().admin, from_chat_id=message.from_user.id,
                                   message_id=message.message_id)
    await message.answer(text='Question send to lecturer')
    await dialog_manager.reset_stack()

question = Dialog(
    Window(
        Const(text='Insert you question'),
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
            *[SwitchTo(Const(data), id=data,
                       state=SheduleState.__dict__[f"window_{data}"]) for data in item['id']]
        ),
        state=SheduleState.__dict__[f"window_{item['day']}"]
    )
for item in Shedule().data()]

shedule_dialog = Dialog(*lst_window)

async def router(dp: Dispatcher):

    @dp.message(Command('question'))
    async def question(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(state=Question.start)

    @dp.message(Command('shedule'))
    async def shedule(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(SheduleState.window_today)