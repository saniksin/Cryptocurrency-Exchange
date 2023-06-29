from pycoingecko import CoinGeckoAPI
from py_currency_converter import convert

from apps.exchange.models import Cryptocurrency, FiatCurrency


def update_exchange_rates():
    cg = CoinGeckoAPI()

    # Обновление курсов для криптовалют
    crypto_ids = [crypto.name.lower() for crypto in Cryptocurrency.objects.all() if crypto.name.lower() not in ['usdt', 'usdc']] + ['tether', 'usd-coin']
    crypto_rates = cg.get_price(ids=', '.join(crypto_ids), vs_currencies='usd,pln,rub,uah')

    cryptos_with_names = ["bitcoin", "ethereum"]
    cryptos_with_codes = ["usdc", "usdt"]

    for crypto in Cryptocurrency.objects.all():
        if crypto.name.lower() in cryptos_with_names or crypto.name.lower() in cryptos_with_codes:
            key = crypto.name.lower() if crypto.name.lower() in cryptos_with_names else crypto.code.lower()
            rates = crypto_rates.get(key, {})
            crypto.current_price_usd = rates.get('usd', 0)
            crypto.current_price_pln = rates.get('pln', 0)
            crypto.current_price_uah = rates.get('uah', 0)
            crypto.current_price_rub = rates.get('rub', 0)
            crypto.save()

    # Обновление фиатных валют
    fiat_rates = convert(base='USD', amount=1, to=['PLN', 'RUB', 'UAH'])
    for code, rate in fiat_rates.items():
        FiatCurrency.objects.filter(code=code.upper()).update(current_price_usd=(1/rate))

