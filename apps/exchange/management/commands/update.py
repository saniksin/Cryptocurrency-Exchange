from django.core.management.base import BaseCommand, CommandError
from apps.exchange.tasks import update_exchange_rates

class Command(BaseCommand):
    help = 'Обновляет курсы валют в обменнике'

    def handle(self, *args, **options):
        try:
            update_exchange_rates()
            self.stdout.write(self.style.SUCCESS('Курсы успешно обновлены'))
        except Exception as e:
            raise CommandError(f'Ошибка при обновлении курсов: {e}')
