import operator
from aiogram import Dispatcher, Router
from aiogram.types import Message, CallbackQuery, User, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, callback_data
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const, Format

from app.config.config import TGbot
from app.router import SLRouter

class TaskState(StatesGroup):
    start = State()
    prepod = State()

class GraphTaskScoreCall(callback_data.CallbackData, prefix='p_t'):
    task: str
    score: str
    user_id: str
    name: str


async def task_handler(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    _, task = item_id.split(sep='_')
    keyboard = task_prepod(task=task, user_id=callback.from_user.id, name='Yur')
    name = dialog_manager.dialog_data['name']
    await callback.bot.send_message(chat_id=TGbot().admin, text=f'Task {task} {name}', reply_markup=keyboard)
    await callback.message.edit_text('Task send to lecturer')
    await dialog_manager.reset_stack()

async def get_task(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    # request to dynamodb need!
    tasks = ['S1', 'S2', 'S3', 'K1']
    dialog_manager.dialog_data['name'] = 'Yurick'
    return {'tasks': [(i, f'{event_from_user.id}_{i}') for i in tasks]}

def task_prepod(task: str, user_id: str, name: str, score: int=8):
    builder = InlineKeyboardBuilder()
    buttons: list = [InlineKeyboardButton(text=str(item),
                                              callback_data=GraphTaskScoreCall(task=task,
                                                                               score=str(item),
                                                                               user_id=str(user_id), name=name).pack())
                                                                               for item in range(score)]
    builder.row(*buttons, width=8)
    return builder.as_markup()


task_dialog = Dialog(
    Window(
        Const(text='Select you task'),
        Select(
            Format('{item[0]}'),
            id='task_id',
            item_id_getter=operator.itemgetter(1),
            items='tasks',
            on_click=task_handler
        ),
        state=TaskState.start,
        getter=get_task
    )
)

router = SLRouter()

@router.message(Command('task'))
async def cmd_task(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(TaskState.start, mode=StartMode.RESET_STACK)

@router.callback_query(GraphTaskScoreCall.filter())
async def graph_task_score_call(callback: CallbackQuery,
                                callback_data: GraphTaskScoreCall):
    # UserVar().add_task(user_id=int(callback_data.user_id),
    #                    task=callback_data.task,
    #                    ball=callback_data.score)
    await callback.bot.send_message(chat_id=callback_data.user_id,
                            text='{task} - {score}'.format(task=callback_data.task,
                                                                        score=callback_data.score))
    await callback.message.edit_text(
        text='{name} - {task}: {score}'.format(name=callback_data.name,
                        score=callback_data.score,
                        task=callback_data.task))