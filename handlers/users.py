import operator
from aiogram import F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hide_link
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, Select, Back

from app.router import SLRouter
from app.config.config import COMMANDS, USER, BUTTON
from app.keyboard.reply import ReplyButton
from app.keyboard.inline import UserInline
from app.connect.api_user import UserApi
from app.filters.user import UserReply

class VideoSelector(StatesGroup):
    category = State()
    video = State()
    view = State()

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

router = SLRouter()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # register = UserUn()
    # register.put_item(user_id=message.from_user.id, name=message.from_user.first_name)
    # buttons = UserButton().unauth_user()
    await message.reply(text=COMMANDS['start'].format(name=message.from_user.first_name),)
                        # reply_markup=buttons)

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

@router.message(UserReply('metodic'))
async def button_metodic(message: Message):
    builder = UserInline(width=2).metodic()
    await message.answer(USER['metodic'], reply_markup=builder)
    await message.delete()

@router.message(UserReply('textbook'))
async def button_book(message: Message):
    builder = UserInline().textbook()
    await message.answer(USER['textbook'], reply_markup=builder)
    await message.delete()

@router.message(UserReply('video'))
async def button_book(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(VideoSelector.category)
    await message.delete()