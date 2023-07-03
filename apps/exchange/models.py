from django.db import models

from apps.users.models import User


# Изменение имени картинки и путь к сохранению
def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.name, filename)


# Криптовалюта
class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    image = models.ImageField(upload_to=upload_to)
    current_price_usd = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)
    current_price_pln = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)  
    current_price_rub = models.DecimalField(max_digits=20, decimal_places=10, default=0.0) 
    current_price_uah = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)
    reception_address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Криптовалюта"
        verbose_name_plural = "Криптовалюты"


# Фиатная валюта    
class FiatCurrency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    image = models.ImageField(upload_to=upload_to)
    # курс валюты к доллару США
    current_price_usd = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)
    reception_address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фиат"
        verbose_name_plural = "Фиатные валюты"


# Транзакция
class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Waiting', 'Ожидает оплаты'),
        ('Cancel', 'Отменена'),
        ('UserPaid', 'Оплачена пользователем'),
        ('Finish', 'Завершена'),
    ]
    
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    unique_transaction_number = models.CharField(max_length=40, unique=True)
    selling_currency = models.CharField(max_length=100)
    selling_amount = models.DecimalField(max_digits=20, decimal_places=10)
    buying_currency = models.CharField(max_length=100)
    buying_amount = models.DecimalField(max_digits=20, decimal_places=10)
    user_reception_address = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Waiting')
    reception_address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

