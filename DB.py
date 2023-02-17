import sqlite3
import datetime

con = sqlite3.connect("baza.db")
cur = con.cursor()


def newUser(name, telegramID):
    cur.execute(f"""INSERT INTO interns VALUES
        ('{name}', '{datetime.date.today()}, '{telegramID}') """)
    con.commit()
    cur.execute("""CREATE TABLE IF NOT EXIST """)

def deleteUser(telegramID):
    cur.execute(f"""DELETE FROM interns WHERE TelegramID = '{telegramID}'""")
    con.commit()