import operator
from aiogram import Dispatcher, Router
from aiogram.types import Message, CallbackQuery, User
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Const, Format

from app.config.config import TGbot, StudyConfig, USER
from app.router import SLRouter
from app.keyboard.inline import GraphTaskScoreCall, AdminInline
from app.filters.user import UserReply
from app.connect.db_students import DBStudents
from app.middleware.user import StudentsMessageMiddleware

class TaskState(StatesGroup):
    start = State()
    prepod = State()

async def task_handler(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, task_id: str):
    name = dialog_manager.dialog_data['name'].split(sep=' ')
    data_name = f"{name[0]} {'.'.join([item[:1] for item in name[1:]])}."
    keyboard = AdminInline(width=8).task_prepod(task=task_id, user_id=callback.from_user.id, name=data_name)
    await callback.bot.send_message(chat_id=TGbot.admin,
                                    text=USER['graph_task_prepod'].format(task=task_id, name=dialog_manager.dialog_data['name']),
                                    reply_markup=keyboard)
    await callback.message.edit_text(USER['graph_task_call'].format(task=task_id))
    await dialog_manager.done()

async def get_task(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    data = DBStudents().get_user(event_from_user.id)
    tasks = list(StudyConfig.tasks)
    for item in data['tasks'].keys():
        tasks.remove(item)
    dialog_manager.dialog_data['name'] = data['name']
    return {'tasks': [(i, i) for i in tasks]}


task_dialog = Dialog(
    Window(
        Const(text=USER['graph_task']),
        Group(
            Select(
                Format('{item[0]}'),
                id='task_id',
                item_id_getter=operator.itemgetter(1),
                items='tasks',
                on_click=task_handler
            ),
            width=6
        ),
        state=TaskState.start,
        getter=get_task
    )
)

router = SLRouter()
router.message.outer_middleware(StudentsMessageMiddleware())
# router.callback_query.outer_middleware(StudentsMessageMiddleware())

@router.message(UserReply('graph_task'))
async def button_task(message: Message, dialog_manager: DialogManager):
    await dialog_manager.reset_stack()
    await dialog_manager.start(TaskState.start, mode=StartMode.RESET_STACK)

@router.callback_query(GraphTaskScoreCall.filter())
async def graph_task_score_call(callback: CallbackQuery,
                                callback_data: GraphTaskScoreCall):
    DBStudents().add_task(user_id=int(callback_data.user_id),
                       task=callback_data.task,
                       ball=callback_data.score)
    await callback.bot.send_message(chat_id=callback_data.user_id,
                            text=USER['graph_task_score_user'].format(task=callback_data.task,
                                                                        score=callback_data.score))
    await callback.message.edit_text(
        text=USER['graph_task_score_prepod'].format(name=callback_data.name,
                        score=callback_data.score,
                        task=callback_data.task))