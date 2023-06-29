from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from apps.reviews.models import Review
from apps.exchange.models import Cryptocurrency, FiatCurrency, Transaction
from apps.exchange.forms import ExchangeForm
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# Главная страница
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_reviews = Review.objects.order_by('-created_at')[:5]
        cryptocurrencies = Cryptocurrency.objects.all()
        fiat_currencies = FiatCurrency.objects.all()
        context['reviews'] = latest_reviews
        context['cryptocurrencies'] = cryptocurrencies
        context['fiat_currencies'] = fiat_currencies
        context['MIN_DEAL'] = settings.MIN_DEAL
        context['MAX_DEAL'] = settings.MAX_DEAL
        return context


# АМL информация
class AmlView(TemplateView):
    template_name = 'aml.html'


# Правила обмена
class RulesView(TemplateView):
    template_name = 'rules.html'


# Предупреждения
class NoticeView(TemplateView):
    template_name = 'notice.html'


def confirm(request):
    context = {}
    context['MIN_DEAL'] = settings.MIN_DEAL
    context['MAX_DEAL'] = settings.MAX_DEAL

    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            try:
                currency = Cryptocurrency.objects.get(code=form.cleaned_data['selling_currency'])
            except ObjectDoesNotExist:
                currency = FiatCurrency.objects.get(code=form.cleaned_data['selling_currency'])
                
            transaction = Transaction.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=form.cleaned_data['email'],
                unique_transaction_number=form.cleaned_data['transaction_id'],
                selling_currency=form.cleaned_data['selling_currency'],
                selling_amount=form.cleaned_data['selling_amount'],
                buying_currency=form.cleaned_data['buying_currency'],
                buying_amount=form.cleaned_data['buying_amount'],
                user_reception_address=form.cleaned_data['receiving_address'],
                recipient_name=form.cleaned_data['recipient_name'],
                reception_address=currency.reception_address,
            )

            return redirect('transaction_info', unique_transaction_number=transaction.unique_transaction_number)
        
    else:
        # Изменение списка на единственное значение для каждого параметра, где это возможно
        initial_data = dict(request.GET)
        for key in initial_data:
            if len(initial_data[key]) == 1:
                initial_data[key] = initial_data[key][0]
        if request.user.is_authenticated:
            form = ExchangeForm(initial={**initial_data, 'email': request.user.email})
        else:
            form = ExchangeForm(initial=initial_data)

    return render(request, 'transaction_confirm.html', {'form': form, **context})



# Окно информации о созданной транзакции
def transaction_info(request, unique_transaction_number):
    if request.method == 'GET':
        transaction = Transaction.objects.get(unique_transaction_number=unique_transaction_number)
        return render(request, 'transaction_info.html', {'transaction': transaction})


# Пользователь переводит транзакцию в статус "Оплачено"
def mark_transaction_as_paid(request, unique_transaction_number):
    transaction = get_object_or_404(Transaction, unique_transaction_number=unique_transaction_number)
    transaction.status = 'UserPaid'
    transaction.save()
    messages.success(request, 'Вы отметили транзакцию как оплаченную. Ожидайте оплаты администратором')
    return redirect('transaction_info', unique_transaction_number=transaction.unique_transaction_number)


# Пользователь переводит транзакцию в статус "Отменено"
def cancel_transaction(request, unique_transaction_number):
    transaction = get_object_or_404(Transaction, unique_transaction_number=unique_transaction_number)
    transaction.status = 'Cancel'
    transaction.save()
    messages.error(request, 'Вы отменили транзакцию.')
    return redirect('index')