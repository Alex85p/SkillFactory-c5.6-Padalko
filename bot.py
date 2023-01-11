import telebot
from config import keys, TOKEN
from extensions import ConvertException, ValueConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы узнать стоимость конвертации валюты,\n\
необходимо отправить сообщение боту в виде:\n\
<имя валюты, цену которой надо узнать> \
 <имя валюты, в которой надо узнать цену первой валюты> \
 <количество первой валюты> \n \nСписок доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convertation(message: telebot.types.Message):
    txt = message.text.lower()
    for i in keys.keys():
        if i in txt:
            try:
                val = txt.split()
                if len(val) != 3:
                    raise ConvertException('Слишком много параметров.')
                quote, base, amount = val
                total = ValueConverter.get_price(quote, base, amount)
            except ConvertException as e:
                bot.reply_to(message, f'Ошибка пользователя \n{e}')
            except Exception as e:
                bot.reply_to(message, f'Не удалось обработать команду \n{e}')
            else:
                text = f'Цена {amount} единиц валюты {quote} в валюте {base} = {round(total, 2)}'
                bot.reply_to(message, text)
            break


bot.polling()
