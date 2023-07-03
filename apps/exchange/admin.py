from django.contrib import admin

from apps.exchange.models import Cryptocurrency, FiatCurrency, Transaction


# Модель Криптовалют
@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


# Модель Фиатных валют
@admin.register(FiatCurrency)
class FiatCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


# Модель транзакций
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'recipient_name', 'unique_transaction_number', 'status', 'date')
    search_fields = ('user__username', 'email', 'unique_transaction_number', 'status', 'date')
    list_filter = ('status', 'date')
    ordering = ('-date',) 

