import operator
from aiogram import F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, Select, Back, Url, Row, SwitchTo, Group

from app.router import SLRouter
from app.config.config import COMMANDS, USER, BUTTON, StudyConfig
from app.keyboard.reply import ReplyButton
from app.keyboard.inline import UserInline
from app.connect.api_user import UserApi
from app.filters.user import UserReply
from app.connect.db_user import DBUser

class VideoSelector(StatesGroup):
    category = State()
    video = State()
    view = State()

class BookSelector(StatesGroup):
    category = State()
    textbook = State()
    metodic = State()

async def category_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['video_category'] = item_id
    await dialog_manager.next()

async def video_selection(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['video_id'] = int(item_id)
    await dialog_manager.next()

async def get_video_category(**kwargs):
    video_categories = UserApi().video_request()
    categories = [(BUTTON[i], i) for i in video_categories.keys()]
    return {'categories': categories}

async def get_video_list(dialog_manager: DialogManager, **kwargs):
    category = dialog_manager.dialog_data['video_category']
    video_request = UserApi().video_request(category)
    video = [(item[0], i) for i, item in enumerate(video_request)]
    return {'video': video}

async def get_video_clip(dialog_manager: DialogManager, **kwargs):
    category = dialog_manager.dialog_data['video_category']
    video_id = dialog_manager.dialog_data['video_id']
    video_request = UserApi().video_request(category)
    return {
        'lab': USER['lab'],
        'category' : BUTTON[category],
        'url': video_request[video_id][1],
        'name': video_request[video_id][0]
        }

async def get_book_category(dialog_manager: DialogManager, **kwargs):
    category = [(BUTTON[item], item) for item in ('metodic', 'textbook')]
    return {
        'book': category
    }


async def book_selector(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    await dialog_manager.switch_to(BookSelector.__dict__[item_id])

video_dialog = Dialog(
    Window(
        Const(USER['category']),
        Column(
            Select(
                Format('{item[0]}'),
                id='video_cat',
                item_id_getter=operator.itemgetter(1),
                items='categories',
                on_click=category_selection
            )
        ),
        state=VideoSelector.category,
        getter=get_video_category
    ),
    Window(
        Const(USER['video_selector']),
        Column(
            Select(
                Format('{item[0]}'),
                id='video_clip',
                item_id_getter=operator.itemgetter(1),
                items='video',
                on_click=video_selection
            ),
            Back(Const(BUTTON['back']))
        ),
        state=VideoSelector.video,
        getter=get_video_list
    ),
    Window(
        Format('<b>{lab}</b> <i>{category}</i>'),
        Format('"<i>{name}</i>"\n'),
        Format(hide_link('{url}')),
        Back(Const(BUTTON['back'])),
        state=VideoSelector.view,
        getter=get_video_clip
    ),
)


book_url = [Url(text=Const(BUTTON[key]), url=Const(value), id=f'button_{key}')
            for key, value in StudyConfig.books.items()]
metodic_url = [Url(text=Const(BUTTON[key]), url=Const(value), id=f'button_{key}')
            for key, value in StudyConfig.metodic.items()]

book_dialog = Dialog(
    Window(
        Const(USER['book']),
        Row(
            Select(
                Format('{item[0]}'),
                id='book_id',
                item_id_getter=operator.itemgetter(1),
                items='book',
                on_click=book_selector
            ),
        ),
        state=BookSelector.category,
        getter=get_book_category
    ),
    Window(
        Const(USER['textbook']),
        Row(*book_url),
        Back(Const(BUTTON['back'])),
        state=BookSelector.textbook,
    ),
    Window(
        Const(USER['metodic']),
        Group(*metodic_url, width=2),
        SwitchTo(Const(BUTTON['back']), id='back_metodic', state=BookSelector.category),
        state=BookSelector.metodic,
    )
)

router = SLRouter()

@router.message(CommandStart())
async def cmd_start(message: Message):
    name_user = f'{message.from_user.first_name} {message.from_user.last_name}'
    DBUser().put_item(user_id=message.from_user.id, name=name_user)
    buttons = ReplyButton().unauth_user()
    await message.reply(text=COMMANDS['start'].format(name=message.from_user.first_name),
                        reply_markup=buttons)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(text=COMMANDS['help'])

@router.message(Command('contact'))
async def cmd_contacts(message: Message):
    builder = UserInline(width=2).contact()
    await message.answer(COMMANDS['contact'], reply_markup=builder)
    await message.delete()


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    buttons = ReplyButton(width=3)(user_id=message.from_user.id)
    await message.answer(text=COMMANDS['menu'], reply_markup=buttons)
    await message.delete()

@router.message(Command('cancel'), StateFilter(default_state))
async def cmd_cancel(message: Message):
    await message.answer(text=COMMANDS['cancel_not'])

@router.message(Command('cancel'), ~StateFilter(default_state))
async def cmd_cancel_state(message: Message, state: FSMContext):
    await message.answer(text=COMMANDS['cancel'])
    await state.clear()

@router.message(UserReply('book'))
async def button_book(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(BookSelector.category)
    await message.delete()

@router.message(UserReply('video'))
async def button_book(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(VideoSelector.category, mode=StartMode.RESET_STACK)
    await message.delete()