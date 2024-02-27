import telebot
from config import TOKEN, keys
from extensions import APIException, Converter



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = ('Чтобы начать работу с ботом, введите команду в следующем формате: \n <имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой вам нужно узнать цену первой валюты> \
<количество первой валюты> \n Вы можете увидеть список всех доступных валют по команде: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
       values = message.text.split(' ')

       if len(values) != 3:
           raise APIException('Слишком много параметров.')

       quote, base, amount = values
       total_price = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_price}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

