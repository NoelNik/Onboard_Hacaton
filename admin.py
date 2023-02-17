import sqlite3
from telebot import types


con = sqlite3.connect("baza.db")
cur = con.cursor()

def admin(userName):
    answer = f"Пользователь @{userName} хочет использовать бота. Разрешить ему?"
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Даа")
    item2 = types.InlineKeyboardButton("Ноуп")
    markup.add(item1, item2)
    return [answer, markup]

# ну тут что-то доделать ещё
# я хз. тут должна быть асинхронность