from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.config.config import BUTTON


class ReplyButton:
    def __init__(self, width=3, resize_keyboard=True):
        self.width = width
        self.resize_keyboard = resize_keyboard

    def __call__(self, user_id):
        self.user = [{'active': 2}] #UserUn().info_user(user_id)
        if self.user[0]['active'] == 3:
            return self.auth_user(user_id)
        if self.user[0]['active'] == 2:
            return self.auth_user(user_id)
        if self.user[0]['active'] == 1:
            return self.unauth_user()
        return False

    @staticmethod
    def _builder(buttons: list[KeyboardButton], width=3, resize_keyboard=True) -> ReplyKeyboardMarkup:
        kp_build = ReplyKeyboardBuilder()
        kp_build.row(*buttons, width=width)
        return kp_build.as_markup(resize_keyboard=resize_keyboard)

    def user_name(self) -> ReplyKeyboardMarkup:
        available = ['no', 'yes']
        buttons: list[KeyboardButton] = [KeyboardButton(text=BUTTON[item]) for item in available]
        return self._builder(buttons, width=self.width, resize_keyboard=self.resize_keyboard)


    def auth_user(self, user_id) -> ReplyKeyboardMarkup:
        box_button = ['profile', 'metodic', 'textbook', 'graph_task', 'schedule', 'video']
        btn = types.KeyboardButton(text=BUTTON[box_button[0]], web_app=WebAppInfo(url=f'https://d5dvtf5ioi8q69ckjelk.apigw.yandexcloud.net/telegram_bot/bot={user_id}'))
        buttons: list[KeyboardButton] = [btn]
        buttons.extend([KeyboardButton(text=BUTTON[item]) for item in box_button[1:]])
        return self._builder(buttons, width=self.width, resize_keyboard=self.resize_keyboard)

    def admin_user(self) -> ReplyKeyboardMarkup:
        comands = ['mailer', 'stat_info', 'exit_admin']
        buttons: list[KeyboardButton] = [KeyboardButton(text=BUTTON[item]) for item in comands]
        return self._builder(buttons, width=self.width, resize_keyboard=self.resize_keyboard)

    def unauth_user(self) -> ReplyKeyboardMarkup:
        box_button = ['metodic', 'textbook', 'video']
        buttons: list[KeyboardButton] = [KeyboardButton(text=BUTTON[item]) for item in box_button]
        return self._builder(buttons, width=self.width, resize_keyboard=self.resize_keyboard)
