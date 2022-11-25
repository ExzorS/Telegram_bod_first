import requests
import json
from currencies import currencies

class APIException(Exception):
    pass

class СurrencyConveret:
    @staticmethod
    def convert(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Одинаковые валюты переводить нельзя!')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base},\nвоспользуйтесь командой /values, что-бы получить список доступных валют.')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote},\nвоспользуйтесь командой /values, что-бы получить список доступных валют.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_quote = json.loads(r.content)[currencies[quote]] * amount

        return total_quote