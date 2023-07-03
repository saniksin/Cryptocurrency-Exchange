import asyncio

from django.core.management.base import BaseCommand, CommandError

from apps.telegrambot.tasks import start_bot


# Команда для запуска телеграмм бота
class Command(BaseCommand):
    help = 'Запускает бота'

    def handle(self, *args, **options):
        try:
            asyncio.run(start_bot())
            self.stdout.write(self.style.SUCCESS('Бот успешно запущен'))
        except Exception as e:
            raise CommandError(f'Ошибка при запуске бота: {e}')