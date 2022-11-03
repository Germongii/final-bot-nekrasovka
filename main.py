import os
import telebot
import sqlite3
from telebot import types
from telebot.types import InputMediaPhoto
import emoji
import logging
from flask import Flask, request
import psycopg2
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

blocked_address = ['1 вольская дом 6', 'льва яшина 3']
blocked_commands = ['Фото с последней высадки' + emoji.emojize(':framed_picture:'),'Дата и место ближайшей высадки' + emoji.emojize(':spiral_calendar:'), 'О проекте' + emoji.emojize(':white_exclamation_mark:'),'Предложить адресс высадки']
bot = telebot.TeleBot('5630686445:AAGW25GL2-9lVZAYkgImUFHokPVk4IYNkt8')
BOT_TOKEN = '5630686445:AAGW25GL2-9lVZAYkgImUFHokPVk4IYNkt8'
APP_URL = "https://green-nekrasovka-bot-new.herokuapp.com/" + BOT_TOKEN
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)
DB_URI = "postgres://owsnwcywmhtemp:17a9fb07098b89855c4d6264920b868201c6a87b9f603ab6bff6a5fdf6a2770e@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/d8jte3avf69b4"

db_connection = psycopg2.connect(DB_URI,sslmode="require")
db_object = db_connection.cursor()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton('Фото с последней высадки' + emoji.emojize(':framed_picture:'))
    item2 = types.KeyboardButton('Дата и место ближайшей высадки' + emoji.emojize(':spiral_calendar:'))
    item3 = types.KeyboardButton('О проекте' + emoji.emojize(':white_exclamation_mark:'))
    item1 = types.KeyboardButton('Предложить адресс высадки')
    markup.add(item4,item2,item3,item1)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == 'Предложить адресс высадки':
        msg = bot.send_message(message.chat.id, 'Введите адресс высадки или геолокацию')
        bot.register_next_step_handler(msg, fio_step)
    if message.text == 'Дата и место ближайшей высадки' + emoji.emojize(':spiral_calendar:'):
        msg = bot.send_message(message.chat.id, 'Высадки продолжатся весной, а пока вы можете предложить адрес высадки')
    if message.text == 'Фото с последней высадки' + emoji.emojize(':framed_picture:'):
        with open('20-09_1.jpg','rb') as photo1, open('20-09_2.jpg','rb') as photo2, open('20-09_3.jpg','rb') as photo3, open('20-09_4.jpg','rb') as photo4,open('20-09_5.jpg','rb') as photo5:
            bot.send_media_group(message.chat.id, [InputMediaPhoto(photo1), InputMediaPhoto(photo2), InputMediaPhoto(photo3),InputMediaPhoto(photo4), InputMediaPhoto(photo5)])
    if message.text == 'О проекте' + emoji.emojize(':white_exclamation_mark:'):
        msg = bot.send_message(message.chat.id,'Test message')





def fio_step(message):
    input_adress = message.text
    input_id = message.from_user.username
    print(input_adress)
    fl = 0
    for l in blocked_commands:
        if input_adress == l:
            fl = 2
            main(message)
            break
    for i in blocked_address:
        if input_adress == i:
            fl = 1
            msg = bot.send_message(message.chat.id, 'Ксожелению высадка на данном адресе невозможна по техническим причинам')
            break
    if fl == 0:
        db_object.execute("INSERT INTO users(user_id, user_addres) VALUES (%s, %s)", (input_id,input_adress))
        db_connection.commit()
        msg = bot.send_message(message.chat.id, 'Спасибо, ваше предложение записано' + emoji.emojize(':check_mark_button:'))
@server.route(f"/{BOT_TOKEN}",methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "|",200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
bot.polling(none_stop=True)
