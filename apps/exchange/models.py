from django.db import models
from apps.users.models import User

def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.name, filename)

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    image = models.ImageField(upload_to=upload_to)
    current_price = models.DecimalField(max_digits=18, decimal_places=8)

    def __str__(self):
        return self.name
    

class FiatCurrency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    image = models.ImageField(upload_to=upload_to)
    # курс валюты к доллару США
    current_price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name="from_currency")
    to_currency = models.ForeignKey(FiatCurrency, on_delete=models.CASCADE, related_name="to_currency")
    rate = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.from_currency.code} to {self.to_currency.code}"
    

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('P', 'В процессе'),
        ('C', 'Завершена'),
        ('A', 'Отменена'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_currency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    to_currency = models.ForeignKey(FiatCurrency, on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')  # новое поле

    def __str__(self):
        return f"{self.user.username} exchanged {self.amount} {self.from_currency.code} to {self.to_currency.code}"