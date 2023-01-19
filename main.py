import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}
TOKEN = "5979542435:AAF5WNFVAsC8hrTuUJK-O6FxQXNR1aBppt8"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Здравствуйте, у нас вы можете узнать актуальный курс валют!\n\nИнструкция: /help"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = "Для конвертации валют введите запрос в следующем формате: \n\nрубль доллар кол-во конвертируемой валюты \n\nЗапятые между названиями валют и количеством валюты не ставятся." \
    "\n\nДля получения списка всех доступных валют введи команду /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()

