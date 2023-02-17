import telebot
from telebot import types
from config import TOKEN



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
    bot.send_message(message.chat.id, f'С чего вы хотите начать, {message.chat.first_name}</b>',
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_echo(message):
    pass

def start():
    bot.polling()