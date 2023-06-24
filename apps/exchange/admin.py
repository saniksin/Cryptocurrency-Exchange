from django.contrib import admin
from django.contrib import admin
from apps.exchange.models import Cryptocurrency, FiatCurrency, ExchangeRate, Transaction, User

class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'current_price']
    search_fields = ['name', 'code']

admin.site.register(Cryptocurrency, CryptocurrencyAdmin)

class FiatCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'current_price']
    search_fields = ['name', 'code']

admin.site.register(FiatCurrency, FiatCurrencyAdmin)

class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['from_currency', 'to_currency', 'rate']
    list_filter = ['from_currency', 'to_currency']

admin.site.register(ExchangeRate, ExchangeRateAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['from_currency', 'to_currency', 'exchange_rate', 'amount', 'date', 'status']
    list_filter = ['date', 'status']

admin.site.register(Transaction, TransactionAdmin)


