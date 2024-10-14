from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config.config import StudyConfig, BUTTON


class InlineKeyboard:
    def __init__(self, width: int = 3, resize_keyboard: bool = True):
        self.width = width
        self.resize_keyboard = resize_keyboard

    @staticmethod
    def builder_row(buttons: list[InlineKeyboardButton], width: int = 3) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(*buttons, width=width)
        return builder.as_markup()

class UserQuestion(CallbackData, prefix='faq'):
    user_id: int

class GraphTaskScoreCall(CallbackData, prefix='p_t'):
    task: str
    score: str
    user_id: str
    name: str


class AdminInline(InlineKeyboard):
    def question(self, user_id: int) -> InlineKeyboardMarkup:
        buttons: list = [InlineKeyboardButton(text=BUTTON['send'],
                                              callback_data=UserQuestion(user_id=user_id).pack())]
        return self.builder_row(buttons=buttons, width=self.width)

    def task_prepod(self, task: str, user_id: str, name: str, score: int=8):
        buttons: list = [InlineKeyboardButton(text=str(item),
                                                callback_data=GraphTaskScoreCall(task=task,
                                                                                score=str(item),
                                                                                user_id=str(user_id), name=name).pack())
                                                                                for item in range(score)]

        return self.builder_row(buttons=buttons, width=self.width)


class UserInline(InlineKeyboard):
    def contact(self) -> InlineKeyboardMarkup:
        contacts: dict = StudyConfig.contact
        buttons: list = [InlineKeyboardButton(text=BUTTON[key], url=value) for key, value in contacts.items()]
        return self.builder_row(buttons=buttons, width=self.width)

    def metodic(self) -> InlineKeyboardMarkup:
        books: dict = StudyConfig.metodic
        buttons: list = [InlineKeyboardButton(text=BUTTON[key], url=value) for key, value in books.items()]
        return self.builder_row(buttons=buttons, width=self.width)

    def textbook(self) -> InlineKeyboardMarkup:
        books: dict = StudyConfig.books
        buttons: list = [InlineKeyboardButton(text=BUTTON[key], url=value) for key, value in books.items()]
        return self.builder_row(buttons=buttons, width=self.width)
