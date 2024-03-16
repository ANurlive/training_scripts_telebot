import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7093273870:AAEQAeFHJ1P0amSZxKE5Bk3UtzLR_EQ_NgU')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Да', callback_data='yes'),
        types.InlineKeyboardButton('Нет', callback_data='no'))
    bot.send_message(message.chat.id,
                     'Привет, я готов выполнить ваши команды. '
                     'Я могу узнать температуру города, конвертировать валюты. '
                     'Для начала давайте зарегистрируемся (имя, возраст). Хорошо?',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'yes':
        name = None
        conn = sqlite3.connect('bot_db.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment PRIMARY KEY, name varchar(50), age int)')
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(call.message.chat.id, 'Введите ваше имя.')
        bot.register_next_step_handler(call.message, user_name)
    else:
        bot.send_message(call.message.chat.id, 'Хорошо')


def user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите ваш возраст.')
    bot.register_next_step_handler(message, user_age, name)


def user_age(message, name):
    age = int(message.text)
    conn = sqlite3.connect('bot_db.sql')
    cur = conn.cursor()
    cur.execute('INSERT INTO users(name, age) VALUES(?, ?)', (name, age))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список зарегистрированных пользователей:', callback_data='users'))
    bot.send_message(message.chat.id, f'Вы успешно зарегистрированы, {name}!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('bot_db.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Имя: {el[1]}, возраст: {el[2]}\n'
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)

              

# @bot.message_handler()
# def any_message(message):


@bot.message_handler(commands=['message_attributes'])
def begin(message):
    bot.send_message(message.chat.id, message)




bot.infinity_polling()