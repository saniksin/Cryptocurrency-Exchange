from django.db import models


class TelegramUser(models.Model):
    username = models.CharField(max_length=100, unique=False, null=True, blank=True)
    user_id = models.CharField(max_length=100, unique=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
