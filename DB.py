import sqlite3
import datetime

con = sqlite3.connect("baza.db")
cur = con.cursor()


def newUser(name, telegramID):

    cur.execute(f"""INSERT INTO interns (Name, comingData, TelegramID) VALUES 
        ('{name}', '{datetime.date.today()}', '{telegramID}') """)
    con.commit()

    if not cur.execute(f"""SELECT TelegramID FROM interns WHERE TelegramID = '{telegramID}'""").fetchone():
        cur.execute(f"""INSERT INTO interns (Name, comingData, TelegramID) VALUES 
            ('{name}', '{datetime.date.today()}', '{telegramID}') """)
        con.commit()

    

def deleteUser(telegramID):
    cur.execute(f"""DELETE FROM interns WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getExp(telegramID):
    return cur.execute(f"""SELECT exp FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()[0]