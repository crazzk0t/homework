import telebot
from config import TOKEN, keys
from extensions import APIException, ValueConverter

'''телеграм бот, который конвертирует валюты'''

bot = telebot.TeleBot(TOKEN) # инициализация бота через токен

@bot.message_handler(commands=['start', 'help']) #принимает команды /start, /help, выводя правила работы с ботом
def start(message: telebot.types.Message):
    text = f'Работа бота заключается в том, чтобы переводить валюты\n\
Для того, чтобы он заработал, нужно ввести данные в таком порядке:\n\
<имя валюты которую хотите перевести> \
<имя валюты в которую хотите перевести> \
<количество первой валюты> \n\
Для того, чтобы узнать доступные валюты, напишите команду "/value"'
    bot.send_message(message.chat.id, text) # возвращает сообщение

@bot.message_handler(commands=['value']) # показывает, какие валюты сейчас доступны для конвертации
def show_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys(): # перечисление валют из словаря keys, который находится в config.py
        text = '\n'.join((text, key))
    bot.reply_to(message, text) # возвращает сообщение

@bot.message_handler(content_types=['text']) # выдает ответ на запрос конвертации
def convert_values(message: telebot.types.Message):
    try: # трай для проверки на наличие ошибок
        value = message.text.split(' ')
        if len(value) != 3:
            raise APIException('Неверное количество данных')

        base, quote, amount = value # деление сообщения на части
        total_load = ValueConverter.get_price(base, quote, amount) # класс из импорта
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}') # except, вызванный пользователем
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}') # except, вызванный кодом
    else:
        text = f'Цена {amount} {keys[base]} равна {total_load * float(amount)} {keys[quote]}'
        bot.reply_to(message, text) # возвращает сообщение


bot.polling(non_stop=True) # запуск бота