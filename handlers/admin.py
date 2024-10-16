import operator
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Row, Button, Select, Column

from app.router import SLRouter
from app.keyboard.inline import UserQuestion
from app.config.config import TGbot, AdminConfig, ADMIN, BUTTON, USER

class Lecturer(StatesGroup):
    start = State()
    available = State()

class ScoreStat(StatesGroup):
    profile = State()
    group = State()
    students = State()
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

async def get_profile(**kwargs):
    profile = [(item, item) for item in AdminConfig.profile[1:]]
    return {'profile': profile}

async def get_group(dialog_manager: DialogManager, **kwargs):
    # profile = [item for item in AdminConfig.profile]
    profile = dialog_manager.dialog_data['profile']
    group = [(item, item) for item in AdminConfig.mailer[profile]]
    return {'group': group}

async def get_students(**kwargs):
    students = [key for key in BUTTON.items()]
    return {'students': students}

async def profile_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, profile_id: str):
    # if profile_id == 'Все':
    #     await dialog_manager.switch_to(ScoreStat.text)
    # else:
    dialog_manager.dialog_data['profile'] = profile_id
    await dialog_manager.next()

async def group_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, group_id: str):
    dialog_manager.dialog_data['group'] = group_id
    await dialog_manager.next()

async def student_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, students_id: str):
    await callback.message.edit_text(students_id)
    await dialog_manager.reset_stack()

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

score_dialog = Dialog(
    Window(
        Const(ADMIN['score']),
        Select(
                Format('{item[1]}'),
                id='profile',
                item_id_getter=operator.itemgetter(0),
                items='profile',
                on_click=profile_selection
            ),
        state=ScoreStat.profile,
        getter=get_profile
    ),
    Window(
        Const(ADMIN['score_group']),
        Select(
                Format('{item[1]}'),
                id='group',
                item_id_getter=operator.itemgetter(0),
                items='group',
                on_click=group_selection
            ),
        state=ScoreStat.group,
        getter=get_group
    ),
    Window(
        Const(ADMIN['stat_info']),
        Column(
            Select(
                    Format('{item[1]}'),
                    id='student',
                    item_id_getter=operator.itemgetter(0),
                    items='students',
                    on_click=student_selection,

                ),
        ),
        state=ScoreStat.students,
        getter=get_students
    ),

)
    # Window(
    #     Const(ADMIN['mailer']),
    #     TextInput(
    #         id='user_input',
    #         # type_factory=user_check,
    #         # on_success=correct_text,
    #         # on_error=error_text
    #     ),
    #     Button(
    #         Const(BUTTON['exit']),
    #         id='exit',
    #         # on_click=exit_user
    #     ),
    #     state=Mailer.text
    # ),
    # Window(
    #     Format(USER['available']),
    #     Row(
    #         # Button(text=Const(BUTTON['yes']), id='yes', on_click=success_register),
    #         # Button(text=Const(BUTTON['no']), id='no', on_click=unsuccess_register)
    #     ),
    #     # getter=get_user,
    #     state=Mailer.available
    # )


router = SLRouter()

@router.callback_query(UserQuestion.filter())
async def send_question(callback: CallbackQuery, callback_data: UserQuestion, dialog_manager: DialogManager):
    await dialog_manager.start(state=Lecturer.start)
    dialog_manager.dialog_data['user_id'] = callback_data.user_id
    await callback.answer()

@router.message(Command('score'))
async def score_query(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=ScoreStat.profile)