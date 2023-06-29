from decimal import Decimal, InvalidOperation
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.exchange.models import Cryptocurrency, FiatCurrency
from django.conf import settings


@api_view(['GET'])
def exchange_rate(request):
    from_code = request.GET.get('from')
    to_code = request.GET.get('to')
    try:
        amount = Decimal(request.GET.get('amount', '1'))
    except InvalidOperation:
        return Response({'error': 'Передаваемый параметр должен быть числом!'}, status=400)

    try:
        from_currency = Cryptocurrency.objects.get(code=from_code)
    except ObjectDoesNotExist:
        from_currency = FiatCurrency.objects.get(code=from_code)

    try:
        to_currency = Cryptocurrency.objects.get(code=to_code)
    except ObjectDoesNotExist:
        to_currency = FiatCurrency.objects.get(code=to_code)

    rate = Decimal(from_currency.current_price_usd / to_currency.current_price_usd)
    result = amount * rate * (1 - settings.EXCHANGE_FEE)

    # Считает эквивалент сделки в USD (сколько получит пользователь)
    usd_equivalent = amount * from_currency.current_price_usd * (1 - settings.EXCHANGE_FEE)

    return Response({'result': result, 'usd_equivalent': usd_equivalent})

