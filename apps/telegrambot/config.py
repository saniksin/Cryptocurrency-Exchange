from aiogram import Bot
from django.conf import settings

bot = Bot(token=settings.TELEGRAM_API)
admin = settings.ADMIN_ID