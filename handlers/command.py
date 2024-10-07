import operator
from aiogram import Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, User
from aiogram.filters import CommandStart, Command

from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Select, Group, Checkbox, ManagedCheckbox, Column, Multiselect, Radio
from aiogram_dialog.widgets.text import Const, Format

class StartStorage(StatesGroup):
    start = State()

class Tech(StatesGroup):
    tech = State()

class News(StatesGroup):
    start = State()

class Language(StatesGroup):
    start = State()

async def yes_click_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await callback.message.edit_text('<b>Succesful</b> This is wonderfull!')
    await dialog_manager.done()

async def no_click_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await callback.message.edit_text('<b>Unuccesful</b> I`m lied!')
    await dialog_manager.done()

async def select_catogory(callback: CallbackQuery, checkbox: ManagedCheckbox, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(is_checked=checkbox.is_checked())

async def user_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'username': event_from_user.username}

async def get_category(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.dialog_data.get('is_checked')
    return {'checked': checked,
            'not_checked': not checked}

async def get_topics(dialog_manager: DialogManager, **kwargs):
    topics = [
        ("IT", '1'),
        ("Дизайн", '2'),
        ("Наука", '3'),
        ("Общество", '4'),
        ("Культура", '5'),
        ("Искусство", '6'),
    ]
    return {'topics': topics}

async def get_language(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.find('radio_lang').get_checked()
    language = {
        '1': 'en',
        '2': 'ru',
        '3': 'fr'
    }
    chosen_lang = language['2' if not checked else checked]
    lang = {
        'ru': {
            '1': '🇬🇧 Английский',
            '2': '🇷🇺 Русский',
            '3': '🇫🇷 Французский',
            'text': 'Выберите язык'
        },
        'en': {
            '1': '🇬🇧 English',
            '2': '🇷🇺 Russian',
            '3': '🇫🇷 French',
            'text': 'Choose language'
        },
        'fr': {
            '1': '🇬🇧 Anglais',
            '2': '🇷🇺 Russe',
            '3': '🇫🇷 Français',
            'text': 'Choisissez la langue'
        }
    }
    languages = [
        (f"{lang[chosen_lang]['1']}", '1'),
        (f"{lang[chosen_lang]['2']}", '2'),
        (f"{lang[chosen_lang]['3']}", '3'),
    ]
    return {'languages': languages,
            'text': lang[chosen_lang]['text']}

start_dialog = Dialog(
    Window(
        Format('Hello, {username}! \n'),
        Const('Can yoy make chat-bot with aiogram?'),
        Row(
            Button(text=Const('[^] Yes'), id='yes', on_click=yes_click_handler),
            Button(text=Const('[?] No'), id='no', on_click=no_click_handler)
        ),
        getter=user_getter,
        state=StartStorage.start
    ),
)

tech_dialog = Dialog(
    Window(
        Const(text='Image working of widget <code>Checkbox</code>\n'),
        Const('No text', when='not_checked'),
        Const('Add text user', when='checked'),
        Checkbox(
            checked_text=Const('[✔️] Отключить'),
            unchecked_text=Const('[ ] Включить'),
            id='checkbox',
            default=False,
            on_state_changed=select_catogory,
        ),
        state=Tech.tech,
        getter=get_category
    ),
)

news_dialog = Dialog(
    Window(
        Const(text='Select thems of news'),
        Column(
            Multiselect(
                checked_text=Format('[✔️] {item[0]}'),
                unchecked_text=Format('[  ] {item[0]}'),
                id='multi_topics',
                item_id_getter=operator.itemgetter(1),
                items='topics',
            )
        ),
        state=News.start,
        getter=get_topics
    )
)

lang_dialog = Dialog(
    Window(
        Format(text='{text}'),
        Column(
            Radio(
                checked_text=Format('🔘 {item[0]}'),
                unchecked_text=Format('⚪️ {item[0]}'),
                id='radio_lang',
                item_id_getter=operator.itemgetter(1),
                items='languages',
            )
        ),
        state=Language.start,
        getter=get_language
    ),
)

async def router(dp: Dispatcher):

    @dp.message(CommandStart())
    async def start(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(state=StartStorage.start, mode=StartMode.RESET_STACK)

    @dp.message(Command(commands=['tech']))
    async def tech(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(Tech.tech)

    @dp.message(Command('news'))
    async def news(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(News.start)

    @dp.message(Command('lang'))
    async def lang(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(Language.start)