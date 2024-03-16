import telebot
from currency_converter import CurrencyConverter
from telebot import types

converter=CurrencyConverter()
amount=0
bot = telebot.TeleBot('7093273870:AAEQAeFHJ1P0amSZxKE5Bk3UtzLR_EQ_NgU')

@bot.message_handler(commands=['currency'])
def convert(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount=int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный формат суммы. Попробуйте снова.')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup=types.InlineKeyboardMarkup(row_width=2)
        btn1=types.InlineKeyboardButton('KZT/USD', callback_data='KZT/USD')
        btn2=types.InlineKeyboardButton('KZT/EUR', callback_data='KZT/EUR')
        btn3=types.InlineKeyboardButton('KZT/RUB', callback_data='KZT/RUB')
        btn4=types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Cумма должна быть больше нуля. Попробуйте снова.')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values=call.data.split('/')
        global amount
        res=converter.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается {round(res, 2)}. Можете еще ввести сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэш')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values=message.text.strip().upper().split('/')
        global amount
        res=converter.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается {round(res, 2)}. Можете еще ввести сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Неправильный формат валют. Попробуйте снова ввести пару значений через слэш.')
        bot.register_next_step_handler(message, my_currency)

bot.infinity_polling()
