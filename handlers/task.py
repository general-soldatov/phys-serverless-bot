import operator
from aiogram import Dispatcher, Router
from aiogram.types import Message, CallbackQuery, User
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Const, Format

from app.config.config import TGbot, USER
from app.router import SLRouter
from app.keyboard.inline import GraphTaskScoreCall, AdminInline
from app.filters.user import UserReply

class TaskState(StatesGroup):
    start = State()
    prepod = State()

async def task_handler(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, task_id: str):
    name = dialog_manager.dialog_data['name']
    keyboard = AdminInline(width=8).task_prepod(task=task_id, user_id=callback.from_user.id, name='Yur')
    await callback.bot.send_message(chat_id=TGbot.admin,
                                    text=USER['graph_task_prepod'].format(task=task_id, name=name),
                                    reply_markup=keyboard)
    await callback.message.edit_text(USER['graph_task_call'].format(task=task_id))
    await dialog_manager.done()

async def get_task(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    # request to dynamodb need!
    tasks = ['S1', 'S2', 'S3', 'K1']
    dialog_manager.dialog_data['name'] = 'Yurick'
    return {'tasks': [(i, i) for i in tasks]}


task_dialog = Dialog(
    Window(
        Const(text=USER['graph_task']),
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

@router.message(UserReply('graph_task'))
async def cmd_task(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(TaskState.start, mode=StartMode.RESET_STACK)

@router.callback_query(GraphTaskScoreCall.filter())
async def graph_task_score_call(callback: CallbackQuery,
                                callback_data: GraphTaskScoreCall):
    # UserVar().add_task(user_id=int(callback_data.user_id),
    #                    task=callback_data.task,
    #                    ball=callback_data.score)
    await callback.bot.send_message(chat_id=callback_data.user_id,
                            text=USER['graph_task_score_user'].format(task=callback_data.task,
                                                                        score=callback_data.score))
    await callback.message.edit_text(
        text=USER['graph_task_score_prepod'].format(name=callback_data.name,
                        score=callback_data.score,
                        task=callback_data.task))