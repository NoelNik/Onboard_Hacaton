import sqlite3
import datetime

con = sqlite3.connect("baza.db")
cur = con.cursor()


def newUser(name):
    cur.execute(f"""INSERT INTO interns VALUES
        ('{name}', '{datetime.date.today()}') """)
    con.commit()


def deleteUser(name):
    cur.execute(f"""DELETE FROM interns WHERE name = '{name}'""")
    con.commit()

