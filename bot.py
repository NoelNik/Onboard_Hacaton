import telebot
from telebot import types
from config import TOKEN



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.chat.id, "COCI")


def start():
    bot.polling()