from aiogram import Dispatcher, Router
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.dispatcher.event.event import EventObserver
from typing import Dict, Optional, List


class SLRouter(Router):
    def __init__(self, *, name: Optional[str] = None):
        """
        :param name: Optional router name, can be useful for debugging
        """

        self.name = name or hex(id(self))

        self._parent_router: Optional[Router] = None
        self.sub_routers: List[Router] = []

        # Observers
        self.message = TelegramEventObserver(router=self, event_name="message")
        self.edited_message = TelegramEventObserver(router=self, event_name="edited_message")
        # self.channel_post = TelegramEventObserver(router=self, event_name="channel_post")
        # self.edited_channel_post = TelegramEventObserver(
        #     router=self, event_name="edited_channel_post"
        # )
        # self.inline_query = TelegramEventObserver(router=self, event_name="inline_query")
        # self.chosen_inline_result = TelegramEventObserver(
        #     router=self, event_name="chosen_inline_result"
        # )
        self.callback_query = TelegramEventObserver(router=self, event_name="callback_query")
        # self.shipping_query = TelegramEventObserver(router=self, event_name="shipping_query")
        # self.pre_checkout_query = TelegramEventObserver(
        #     router=self, event_name="pre_checkout_query"
        # )
        # self.poll = TelegramEventObserver(router=self, event_name="poll")
        # self.poll_answer = TelegramEventObserver(router=self, event_name="poll_answer")
        self.my_chat_member = TelegramEventObserver(router=self, event_name="my_chat_member")
        self.chat_member = TelegramEventObserver(router=self, event_name="chat_member")
        # self.chat_join_request = TelegramEventObserver(router=self, event_name="chat_join_request")
        self.message_reaction = TelegramEventObserver(router=self, event_name="message_reaction")
        self.message_reaction_count = TelegramEventObserver(
            router=self, event_name="message_reaction_count"
        )
        # self.chat_boost = TelegramEventObserver(router=self, event_name="chat_boost")
        # self.removed_chat_boost = TelegramEventObserver(
        #     router=self, event_name="removed_chat_boost"
        # )
        # self.deleted_business_messages = TelegramEventObserver(
        #     router=self, event_name="deleted_business_messages"
        # )
        # self.business_connection = TelegramEventObserver(
        #     router=self, event_name="business_connection"
        # # )
        # self.edited_business_message = TelegramEventObserver(
        #     router=self, event_name="edited_business_message"
        # )
        # self.business_message = TelegramEventObserver(router=self, event_name="business_message")

        self.errors = self.error = TelegramEventObserver(router=self, event_name="error")

        self.startup = EventObserver()
        self.shutdown = EventObserver()

        self.observers: Dict[str, TelegramEventObserver] = {
            "message": self.message,
            "edited_message": self.edited_message,
            # "channel_post": self.channel_post,
            # "edited_channel_post": self.edited_channel_post,
            # "inline_query": self.inline_query,
            # "chosen_inline_result": self.chosen_inline_result,
            "callback_query": self.callback_query,
            # "shipping_query": self.shipping_query,
            # "pre_checkout_query": self.pre_checkout_query,
            # "poll": self.poll,
            # "poll_answer": self.poll_answer,
            "my_chat_member": self.my_chat_member,
            # "chat_member": self.chat_member,
            # "chat_join_request": self.chat_join_request,
            "message_reaction": self.message_reaction,
            "message_reaction_count": self.message_reaction_count,
            # "chat_boost": self.chat_boost,
            # "removed_chat_boost": self.removed_chat_boost,
            # "deleted_business_messages": self.deleted_business_messages,
            # "business_connection": self.business_connection,
            # "edited_business_message": self.edited_business_message,
            # "business_message": self.business_message,
            "error": self.errors,
        }


    # def message(self, func):
    #     def wrapped(*args):
    #         self.funcs.append([func, args])
    #     return wrapped

    # def callback_query(self, func):
    #     def wrapped(*args):
    #         self.funcs.append([func, args])
    #     return wrapped
