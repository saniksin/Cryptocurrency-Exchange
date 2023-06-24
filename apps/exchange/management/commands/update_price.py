# from django.core.management.base import BaseCommand
# from exchange.models import Cryptocurrency
# import requests
# import json


# def get_crypto_price(code):
#     response = requests.get(f'https://api.binance.com/api/v3/depth?limit=1&symbol={code}USDT')
#     data = json.loads(response.text)
#     return data["bids"][0][0]


# class Command(BaseCommand):
#     help = 'Update prices of all cryptocurrencies'

#     def handle(self, *args, **options):
#         for crypto in Cryptocurrency.objects.all():
#             price = get_crypto_price(crypto.code)
#             crypto.current_price = price
#             crypto.save()