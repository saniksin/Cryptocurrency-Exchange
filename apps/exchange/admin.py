from django.contrib import admin
from django.contrib import admin
from apps.exchange.models import Cryptocurrency, FiatCurrency, Transaction

@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(FiatCurrency)
class FiatCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'recipient_name', 'unique_transaction_number', 'status', 'date')
    search_fields = ('user__username', 'email', 'unique_transaction_number', 'status', 'date')
    list_filter = ('status', 'date')
    ordering = ('-date',) 


