import telebot
import requests
import json

TOKEN = '7441235956:AAEyzASxgMT3-XcpOvIfgF-98mRJvdmmgbI'

bot = telebot.TeleBot(TOKEN)

keys = {"bitcoin":"BTC",
        "ethirium":"ETH",
        "dollar":"USD"}

@bot.message_handler(commands=['start'])
def greeting(message: telebot.types.Message):
    bot.reply_to(message, f'Hello, {message.chat.username}')

@bot.message_handler(commands=['help'])
def hepler(message: telebot.types.Message):
    text = 'To use the bot write a command similarly like on an example\n<Name of a value>\
<value to convert>\
<number>\n\
To see all the values write "/value"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['value'])
def show_values(message: telebot.types.Message):
    text = 'Available values: '
    for key in keys.keys():
        text = f'\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_load = json.loads(r.content)[keys[base]]
    text = f'The price of {amount} {quote} is equal to {total_load}'
    bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)