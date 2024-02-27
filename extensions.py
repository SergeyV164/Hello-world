import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/e80c519591e79de9771b78ac/pair/{quote_ticker}/{base_ticker}')
        total_price = json.loads(r.content)["conversion_rate"] * int(amount)
        return  total_price