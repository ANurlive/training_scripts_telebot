import telebot
import requests
import json
from telebot import types

bot = telebot.TeleBot('7093273870:AAEQAeFHJ1P0amSZxKE5Bk3UtzLR_EQ_NgU')
API='54681c2e6e01c942cb693cd05705c0b9'

@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Введите название города (на английском):')
    bot.register_next_step_handler(message, get)

def get(message):
    city=message.text.strip().lower()
    res=requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code==200:
        data=json.loads(res.text)
        bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]} градусов Цельсия')
        markup=types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('Да', callback_data='yes'),
            types.InlineKeyboardButton('Нет', callback_data='no'))
        bot.send_message(message.chat.id, 'Хотите узнать погоду еще одного города?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data=='yes':
        bot.send_message(call.message.chat.id, 'Введите название города')
        bot.register_next_step_handler(call.message, get)
    else:
        bot.reply_to(call.message, 'Неправильно введено название города. Попробуйте снова')
        bot.register_next_step_handler(call.message, get)

bot.polling()

