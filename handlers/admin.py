import operator
import logging
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramAPIError
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Row, Button, Select, Column, Back

from app.router import SLRouter
from app.keyboard.inline import UserQuestion
from app.connect.db_students import DBStudents
from app.config.config import TGbot, AdminConfig, ADMIN, BUTTON, USER

logger = logging.getLogger(__name__)

class Lecturer(StatesGroup):
    start = State()
    available = State()

class ScoreStat(StatesGroup):
    profile = State()
    group = State()
    students = State()
    score = State()

class Mailer(StatesGroup):
    profile = State()
    group = State()
    text = State()
    available = State()

async def get_message_id(message: Message, widget: MessageInput,
                       dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data['message_id'] = message.message_id
    await dialog_manager.next()

async def question_yes(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    user_id = dialog_manager.dialog_data['user_id']
    message_id = dialog_manager.dialog_data['message_id']
    await callback.bot.copy_message(chat_id=user_id, from_chat_id=TGbot.admin, message_id=message_id)
    await callback.message.edit_text(ADMIN['question_succesful'].format(user_id=user_id))
    await dialog_manager.done()

async def mailer_yes(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    profile = dialog_manager.dialog_data['profile']
    group = dialog_manager.dialog_data['group']
    if profile == BUTTON['all']:
        pass
    else:
        user_list = DBStudents().mailer_user(profile, group)
        errors = await mailer_go(callback, user_list, dialog_manager.dialog_data['message_id'])
    await callback.message.edit_text(text=ADMIN['mailer_done'].format(errors=errors))
    await dialog_manager.done()


async def mailer_go(callback: CallbackQuery, user: list, message_id: str | int):
    errors = {}
    if user:
        for item in user:
            try:
                await callback.bot.copy_message(from_chat_id=callback.from_user.id,
                                    chat_id=item,
                                    message_id=message_id)
            except TelegramAPIError as e:
                    if 'Bad Request: chat not found' in e.__str__():
                        # UserUn().update_active(user_id=item, active=0)
                        errors[item] = e
                        logger.error(e)

            except Exception as e:
                logger.error(e)
                errors[item] = e
    else:
        errors['all'] = 'not users'
    return errors


async def get_profile(**kwargs):
    profile = [(item, item) for item in AdminConfig.profile[1:]]
    return {'profile': profile}

async def get_group(dialog_manager: DialogManager, **kwargs):
    profile = dialog_manager.dialog_data['profile']
    group = [(item, item) for item in AdminConfig.mailer[profile]]
    return {'group': group}

async def get_students(dialog_manager: DialogManager, **kwargs):
    profile = dialog_manager.dialog_data['profile']
    group = dialog_manager.dialog_data['group']
    text = lambda item: f"{item['name']}_%{item['prize']}_Score{item['fine']}"
    students = [(text(item), str(item['user_id'])) for item in DBStudents().score_user(profile, group)]
    return {'students': students}

async def get_mail(dialog_manager: DialogManager, **kwargs):
    data = dict(**dialog_manager.dialog_data)
    if not dialog_manager.dialog_data['group']:
        data['group'] = 'All'
    return data

class SelectorStud:
    def __init__(self, stat: StatesGroup, types_data: str):
        self.stat = stat
        self.types_data = types_data

    async def __call__(self, callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, data: str):
        if isinstance(self.stat, Mailer) and self.types_data == 'profile' and data == 'Все':
            await dialog_manager.switch_to(Mailer.text)
        else:
            dialog_manager.dialog_data[self.types_data] = data
            await dialog_manager.next()


def score_check(text: str) -> str:
    condition = (
        text[0] == '%' and 0 <= int(text[1:]) <= 100,
        (text[0] == '-' or text[0] == '+') and int(text[1:]) < 50
    )
    if any(condition):
        return text
    raise ValueError

async def score_correct_text(message: Message, widget: ManagedTextInput,
                       dialog_manager: DialogManager, user_id: str) -> None:
    if message.text[0] == '%':
        student_id = dialog_manager.dialog_data['student_id']
        DBStudents().set_prize(int(student_id), prize=int(message.text[1:]))
    elif message.text[0] in ('+', '-'):
        student_id = dialog_manager.dialog_data['student_id']
        DBStudents().set_fine(int(student_id), fine=int(message.text))
    await message.answer(ADMIN['success_score'])
    await dialog_manager.switch_to(ScoreStat.students)


async def error_text(message: Message, widget: ManagedTextInput,
                     dialog_manager: DialogManager, error: ValueError):
    await message.answer(USER['uncorrect'])

question_dialog = Dialog(
    Window(
        Const(ADMIN['reply_question']),
        MessageInput(get_message_id),
        state=Lecturer.start
    ),
    Window(
        Const(ADMIN['available_reply']),
        Row(
            Button(text=Const(BUTTON['yes']), id='yes', on_click=question_yes),
            Back(text=Const(BUTTON['no']))
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
                on_click=SelectorStud(ScoreStat, 'profile')
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
                on_click=SelectorStud(ScoreStat, 'group')
            ),
        Back(Const(BUTTON['back'])),
        state=ScoreStat.group,
        getter=get_group
    ),
    Window(
        Const(ADMIN['stat_info']),
        Column(
            Select(
                    Format('{item[0]}'),
                    id='student',
                    item_id_getter=operator.itemgetter(1),
                    items='students',
                    on_click=SelectorStud(ScoreStat, 'student_id'),

                ),
        ),
        Back(Const(BUTTON['back'])),
        state=ScoreStat.students,
        getter=get_students
    ),
    Window(
        Const(ADMIN['score_group_case']),
        TextInput(
            id='user_input',
            type_factory=score_check,
            on_success=score_correct_text,
            on_error=error_text
        ),
        state=ScoreStat.score
    )
)

mailer_dialog = Dialog(
    Window(
        Const(ADMIN['mailer']),
        Select(
                Format('{item[1]}'),
                id='profile',
                item_id_getter=operator.itemgetter(0),
                items='profile',
                on_click=SelectorStud(Mailer, 'profile')
            ),
        state=Mailer.profile,
        getter=get_profile
    ),
    Window(
        Const(ADMIN['mail_group']),
        Select(
                Format('{item[1]}'),
                id='group',
                item_id_getter=operator.itemgetter(0),
                items='group',
                on_click=SelectorStud(Mailer, 'group')
            ),
        Back(Const(BUTTON['back'])),
        state=Mailer.group,
        getter=get_group
    ),
    Window(
        Const(ADMIN['message_mailer']),
        MessageInput(get_message_id),
        Back(Const(BUTTON['back'])),
        state=Mailer.text
    ),
    Window(
            Format(ADMIN['available']),
            Row(
                Button(text=Const(BUTTON['yes']), id='yes', on_click=mailer_yes),
                Back(text=Const(BUTTON['no']))
            ),
            getter=get_mail,
            state=Mailer.available
        )
)




router = SLRouter()

@router.callback_query(UserQuestion.filter())
async def send_question(callback: CallbackQuery, callback_data: UserQuestion, dialog_manager: DialogManager):
    await dialog_manager.start(state=Lecturer.start)
    dialog_manager.dialog_data['user_id'] = callback_data.user_id
    await callback.answer()

@router.message(Command('score'))
async def score_query(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=ScoreStat.profile)

@router.message(Command('mail'))
async def score_query(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=Mailer.profile)