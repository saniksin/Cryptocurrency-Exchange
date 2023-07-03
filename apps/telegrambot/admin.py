from django.contrib import admin
from .models import TelegramUser

# Модель ТелеграмЮзера
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'is_blocked')
    search_fields = ('username', 'user_id')

