import telebot
from telebot import types
from config import TOKEN
from DB import getTask, getExp

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Я буду твоим помошником для удобной адаптации к новой рабочей среде")
    sti = open('stickers/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Рассказать про нашу компанию')
    item2 = types.KeyboardButton('Показать свой профиль')
    item3 = types.KeyboardButton('Связь с HR')
    item4 = types.KeyboardButton('Показать задания')

    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, f'С чего вы хотите начать, {message.chat.first_name}',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_echo(message):
    if message.text == "Рассказать про нашу компанию":
        bot.send_message(message.chat.id, "Перейди по ссылке за всей нужной информацией :)")
        bot.send_message(message.chat.id, "https://disk.yandex.ru/d/SO7F8r0xI3DAsg")

    elif message.text == "Показать свой профиль":
        bot.send_message(message.chat.id,
                         f"{message.chat.first_name}, вот сколько у тебя баллов: {getExp(message.chat.id)}")

    elif message.text == "Показать задания":
        bot.send_message(message.chat.id, f"Вот список твоих заданий: {getTask(message.chat.id)}")

    else:
        item1 = types.KeyboardButton('/start')
        item2 = types.KeyboardButton('/help')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Я не понял вашу команду", reply_markup=markup)


def start():
    bot.infinity_polling()
