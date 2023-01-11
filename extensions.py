import requests
import json
from config import keys


class ConvertException(Exception):
    pass


class ValueConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertException('Нельзя конвертировать валюту в саму себя.')

        try:
            float(amount)
        except ValueError:
            raise ConvertException(f'Количество валюты должно быть цифрой, а не текстом.')

        if float(amount) < 0:
            raise ConvertException('Количество валюты должно быть больше 0.')

        try:
            quote_v = keys[quote]
        except KeyError:
            raise ConvertException(f'Валюта {quote} не доступна либо не верно задана')

        try:
            base_v = keys[base]
        except KeyError:
            raise ConvertException(f'Валюта {base} не доступна либо не верно задана')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_v}&tsyms={base_v}')
        total = float(json.loads(r.content)[keys[base]]) * float(amount)

        return total
