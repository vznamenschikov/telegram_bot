# Telegram Bot: Пересчёт курса валют.  Username: https://t.me/EchoVZBoyBot    Bot: EchoVZBoy

import telebot
from vz_config import keys, BOT_TOKEN
from extensions import APIException, get_price, ServerAPIException


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):

    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, )) # Эквивалент строчки ниже
        # text = text + '\n' + key # ВОПРОС К МЕНТОРУ: Подскажите пожалуйста, почему так не пишут? Компактнее, нагляднее
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        # s = [] [s.append(i.lower()) if not i.islower() else s.append(i) for i in values]
        # values = [x.lower() for x in values]              # Преобразование строки ввода в нижний регистр
        # values = list(map(lambda x: x.lower(), values))   # Преобразование строки ввода в нижний регистр
        # values = "%".join(values).lower().split("%")      # Преобразование строки ввода в нижний регистр
        values = list(map(str.lower, values))               # Преобразование строки ввода в нижний регистр

        if len(values) != 3:
            raise APIException('Количество параметров не равняется 3-м.')

        quote, base, amount = values
        # print(f'"{quote},{base},{amount}"')

        total_base = get_price.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Сумма {amount} {keys[quote]} по курсу {quote}-{base} равна {format(total_base, ".2f")} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()