import requests
import json
from vz_config import keys, FIXER_IO_TOKEN

class APIException(Exception):
    pass

class ServerAPIException(Exception):
    pass

class get_price:
    @staticmethod
    def convert(quote: str, base: str, amount: str):



        #if quote == base:
        #    raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        # quote_ticker, base_ticker = keys[quote], keys[base]
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


        # orig r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # По подписке r = requests.get(f'https://data.fixer.io/api/convert?access_key={FIXER_IO_TOKEN}&from={quote_ticker}&to={base_ticker}&amount={amount}')
        # По всем валютам r = requests.get(f'http://data.fixer.io/api/latest?access_key={FIXER_IO_TOKEN}')  # &amount={amount}')
        # base=EUR r = requests.get(f'http://data.fixer.io/api/latest?access_key={FIXER_IO_TOKEN}&base={quote_ticker}&symbols={base_ticker}')
        # Формат ответа: r= [b'{"success":true,"timestamp":1704655923,"base":"EUR","date":"2024-01-07","rates":{"USD":1.09547}}']
        request_success = False

        r = requests.get(f'http://data.fixer.io/api/latest?access_key={FIXER_IO_TOKEN}&base=EUR&symbols={base_ticker}')  # Запрашиваем базовый курс EUR-{base_ticker}
        total_base = json.loads(r.content).get("rates").get(base_ticker)    # Сохраняем курс в total_base
        request_success = bool(json.loads(r.content).get("success"))        # Проверка успешности ответа от сервера: success=True/False

        if request_success:
            if quote_ticker == 'EUR':
               print(f'Курс {quote_ticker}-{base_ticker} - {total_base}')
               total_base = amount * total_base
            else:
               # Базовая валюта на бесплатном аккаунте - только ЕВРО, поэтому пересчитываем по кросс-курсу
               r = requests.get(f'http://data.fixer.io/api/latest?access_key={FIXER_IO_TOKEN}&base=EUR&symbols={quote_ticker}')  # Запрос для расчёта кросс-курса
               cross_rate = json.loads(r.content).get("rates").get(quote_ticker)   # Cохраняем для цепочки EUR->{quote_ticker}->{base_ticker}
               print(f'Пересчитываем по кросс-курсу {quote_ticker}-{base_ticker} - {total_base / cross_rate}')

               # total_base = amount / cross_rate * total_base
               total_base = amount * (total_base / cross_rate)
        else:
            raise ServerAPIException(f'Ошибка ответа от сервера')

        print(f'Результат конвертации: {amount}{keys[quote]} -> {format(total_base, ".2f")}{keys[base]}')

        return total_base

