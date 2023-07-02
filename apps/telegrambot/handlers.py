from aiogram import types
from django.conf import settings
from apps.telegrambot.config import bot, admin
from django.contrib.sites.models import Site
from apps.exchange.models import Transaction
from apps.telegrambot.models import TelegramUser
from asgiref.sync import sync_to_async
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
import re


# Создаем пользователя в бд 
async def get_or_create_user(message: types.Message) -> TelegramUser:
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    try:
        # Проверяем, есть ли пользователь в базе данных
        user = await sync_to_async(TelegramUser.objects.get)(user_id=str(message.from_user.id))

        # Если username доступен и отличается от того, что у нас уже есть, мы его обновляем
        if username != user.username:
            user.username = username
            await sync_to_async(user.save)()
    except ObjectDoesNotExist:
        # Если пользователя нет в базе данных, создаем нового
        user = await sync_to_async(TelegramUser.objects.create)(username=username, user_id=str(message.from_user.id))
        
    return username, user


# Ответ на команду start
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать, я ваш помощник. Пожалуйста, задайте мне свой вопрос, и я передам его администратору!🦄\n"
                        "Если вопрос связан с какой-либо транзакцией сразу указывайте ее номер!")


# Получаем информацию о домене
async def get_domain_info():

    protocol = 'http' if settings.DEBUG else 'https'
    site = await sync_to_async(Site.objects.get_current)()
    domain = site.domain

    return protocol, domain


# Подтвержение на почту
def send_email_notification(email, transaction_number):
    subject = "Ваша транзакция успешно завершена!"
    message = f"Дорогой клиент, ваша транзакция {transaction_number} была успешно завершена админом.\n" \
               "Проверьте поступление оплаты на свой счет!\n" \
               "В случае возникновения вопросов свяжитесь со службой поддержки.\n\n" \
               "Благодарим за использование нашего сервиса!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)


# Сообщаем администратору об созданной транзакции
async def notify_admin(transaction, bot=bot):

    protocol, domain = await get_domain_info()

    message_to_send = (
    f"<b>Транзакция:</b> "
    f"<a href='{protocol}://{domain}/admin/exchange/transaction/{transaction.id}/change/'>{transaction.unique_transaction_number}</a>\n"
    f"<i>(Оплачено пользователем)</i>\n\n"

    f"<b>Email пользователя:</b> {transaction.email}\n\n"

    f"<b>Пользователь продает:</b>\n"
    f"{transaction.selling_amount} {transaction.selling_currency}\n\n"

    f"<b>Проверьте поступление на адрес/карту:</b>\n"
    f"{transaction.reception_address}\n\n"

    f"<b>Пользователь покупает:</b>\n"
    f"{transaction.buying_amount} {transaction.buying_currency}\n\n"

    f"<b>Если перевод от пользователя поступил, переведите средства на карту/адрес:</b>\n"
    f"{transaction.user_reception_address}\n\n"

    f"<b>Имя и фамилия получателя:</b>\n"
    f"{transaction.recipient_name}\n\n"

    f"<i>Пожалуйста, обработайте данную транзакцию.\n</i>"
    f"<i>Отмените транзакцию либо переведите ее в статус завершена!</i>")

    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        types.InlineKeyboardButton("Отменить", callback_data=f'cancel_{transaction.id}'),
        types.InlineKeyboardButton("Завершить", callback_data=f'finish_{transaction.id}'),
    )
    
    await bot.send_message(admin, message_to_send, parse_mode='HTML', reply_markup=inline_keyboard)


# Обрабатываем статус транзакции
async def process_transaction_status(callback_query: types.CallbackQuery, new_status: str, reply_text: str):
    transaction_id = int(callback_query.data.split('_')[1])
    
    transaction = await sync_to_async(Transaction.objects.get)(pk=transaction_id)
    transaction.status = new_status
    await sync_to_async(transaction.save)()

    protocol, domain = await get_domain_info()
    transaction_url = f"{protocol}://{domain}/admin/exchange/transaction/{transaction.id}/change/"

    message = f"{reply_text} <a href='{transaction_url}'>{transaction.unique_transaction_number}</a>"

    await bot.send_message(callback_query.from_user.id, message, parse_mode='HTML')

    if new_status == 'Finish':
        await sync_to_async(send_email_notification)(transaction.email, transaction.unique_transaction_number)

    await bot.answer_callback_query(callback_query.id)


# Отменяем транзакцию
async def process_callback_cancel(callback_query: types.CallbackQuery):
    await process_transaction_status(callback_query, 'Cancel', "Транзакция отменена:")


# Завершаем транзакцию 
async def process_callback_finish(callback_query: types.CallbackQuery):
    await process_transaction_status(callback_query, 'Finish', "Транзакция завершена:")


# Обработчик блокировки/разблокировки
async def toggle_user_block_status(message: types.Message, block: bool):
    user_id = message.get_args()

    queryset = await sync_to_async(TelegramUser.objects.filter)(user_id=user_id)
    user = await sync_to_async(queryset.first)()

    if user:
        user.is_blocked = block
        await sync_to_async(user.save)()

        action = "был заблокирован" if block else "был разблокирован"
        await message.reply(f"Пользователь с ID {user_id} {action}.")
    else:
        await message.reply(f"Пользователь с ID {user_id} не был найден.")


# Блокируем пользоваля
async def block_user(message: types.Message):
    await toggle_user_block_status(message, True)


# Разблокируем пользоваля
async def unblock_user(message: types.Message):
    await toggle_user_block_status(message, False)


# Обрабатываем сообщения от пользователей
async def forward_to_admin(message: types.Message):

    username, user = await get_or_create_user(message)

    # Отправляем форматированное сообщение администратору
    await bot.send_message(
        admin,
        f"Получено новое обращение.\nПользователь: {username} (ID: {user.user_id})\n\nТекст: {message.text}"
    )


# Обрабатываем ответы админа на сообщения от пользователей
async def reply_to_user(message: types.Message):
    if message.reply_to_message is not None:
        original_message = message.reply_to_message

        # Извлечение ID пользователя из сообщения
        user_id = re.search(r"(ID: )(\d+)", original_message.text).group(2)

        await bot.send_message(chat_id=user_id, text=message.text)
