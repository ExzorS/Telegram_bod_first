import telebot
from token_key import TOKEN
from currencies import currencies
from extensions import APIException, СurrencyConveret

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Как пользоваться ботом! \nВводите: \n<КАКУЮ валюту хотите перевести>' \
           ' \n<В КАКУЮ валюту хотите перевести>' \
           ' \n<СКОЛЬКО хотите перевести>' \
           ' \nДоступные вылюты можно увидеть с помощью комманды: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверные параметры!')

        base, quote, amount = values
        total_quote = СurrencyConveret.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_quote}'
        bot.send_message(message.chat.id, text)


bot.polling()

