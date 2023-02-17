import telebot
from telebot import types



bot = telebot.TeleBot(token)


bot.polling()
