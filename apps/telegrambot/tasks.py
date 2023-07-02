from aiogram import Dispatcher
from django.conf import settings
from apps.telegrambot.config import bot, admin
from apps.telegrambot.middleware import AccessMiddleware
from apps.telegrambot.handlers import (
    send_welcome,
    process_callback_cancel, 
    process_callback_finish,
    block_user,
    unblock_user,
    forward_to_admin, 
    reply_to_user,
)


async def start_bot():
    dp = Dispatcher(bot)

    # Проверка на блокировку
    dp.middleware.setup(AccessMiddleware())

    # Команда старт
    dp.register_message_handler(send_welcome, commands=['start'])

    # Отменяем транзакцию
    dp.register_callback_query_handler(process_callback_cancel, lambda c: c.data.startswith('cancel_'))

    # Завершаем тразакцию
    dp.register_callback_query_handler(process_callback_finish, lambda c: c.data.startswith('finish_'))
    
    # Блокируем пользователя
    dp.register_message_handler(block_user, lambda message: str(message.from_user.id) == admin, commands=['block'], commands_prefix='/')

    # Разблокируем пользоваля
    dp.register_message_handler(unblock_user, lambda message: str(message.from_user.id) == admin, commands=['unblock'], commands_prefix='/')

    # Пересылаем сообщение админу
    dp.register_message_handler(forward_to_admin, lambda message: str(message.from_user.id) != admin)

    # Пересылаем ответ админа пользователю
    dp.register_message_handler(reply_to_user, lambda message: str(message.from_user.id) == admin)


    await dp.start_polling()