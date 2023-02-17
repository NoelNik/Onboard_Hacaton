import sqlite3
import datetime
from random import randint

con = sqlite3.connect("baza.db", check_same_thread=False)
cur = con.cursor()


def newUser(name, telegramID):
    if not cur.execute(f"""SELECT TelegramID FROM interns WHERE TelegramID = '{telegramID}'""").fetchone():
        cur.execute(f"""INSERT INTO interns (Name, comingData, TelegramID) VALUES 
            ('{name}', '{datetime.date.today()}', '{telegramID}') """)
        con.commit()


def deleteUser(telegramID):
    cur.execute(f"""DELETE FROM interns WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getExp(telegramID):
    return cur.execute(f"""SELECT exp FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()[0]


def check_for_win(telegramID):
    prize_list = {"first": [], "second": [], "third": []}
    quantity_for_first = 15
    quantity_for_second = 30
    quantity_for_third = 45
    if getExp(telegramID) > quantity_for_first:
        return prize_list["first"][randint(0, len(prize_list["first"]))]

    elif getExp(telegramID) > quantity_for_second:
        return prize_list["second"][randint(0, len(prize_list["second"]))]

    elif getExp(telegramID) > quantity_for_third:
        return prize_list["third"][randint(0, len(prize_list["third"]))]


def getData(telegramID):
    return cur.execute(f"""SELECT comingData FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()[0]


def if_user_exist(telegramID):
    return bool(cur.execute(f"""SELECT TelegramID FROM interns WHERE TelegramID = '{telegramID}'""").fetchone())

def appendQueue(telegramID):
    cur.execute(f"""INSERT INTO queue (TelegramID) VALUES ('{telegramID}')""")
    con.commit()


def appendChatActive(intern, Admin):
    cur.execute(f"""INSERT INTO activeChat (idIntern, idAdmin) VALUES ('{intern}', '{Admin}')""")
    con.commit()

def deleteQueue(telegramID):
    cur.execute(f"""DELETE FROM queue WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getTasks():
    return cur.execute(f"""SELECT * FROM tasks""").fetchall()


def addTask(telegramID, newTask):
    cur.execute(f"""UPDATE interns set task = '{newTask}' WHERE TelegramID = '{telegramID}'""")
    con.commit()
    return "Задание обновлено"
