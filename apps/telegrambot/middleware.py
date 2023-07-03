from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from apps.telegrambot.handlers import get_or_create_user
from apps.telegrambot.models import TelegramUser


# Обработчик сообщений в случае блокировки пользователя
class AccessMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        try:
            user = await sync_to_async(TelegramUser.objects.get)(user_id=message.from_user.id)
            if user.is_blocked:
                await message.reply("Вы заблокированы. У вас больше нету доступа к боту.")
                raise CancelHandler()
        except ObjectDoesNotExist:
            username, user = await get_or_create_user(message)


