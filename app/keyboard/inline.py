from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config.config import BUTTONS_RU


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

class UserInline(InlineKeyboard):
    def question(self, user_id: int) -> InlineKeyboardMarkup:
        buttons: list = [InlineKeyboardButton(text=BUTTONS_RU['send'],
                                              callback_data=UserQuestion(user_id=user_id).pack())]
        return self.builder_row(buttons=buttons, width=self.width)