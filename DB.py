import sqlite3
import datetime
from random import randint

con = sqlite3.connect("baza.db", check_same_thread=False)
cur = con.cursor()


def newUser(telegramID):
    if not cur.execute(f"""SELECT TelegramID FROM interns WHERE TelegramID = '{telegramID}'""").fetchone():
        cur.execute(f"""INSERT INTO interns (comingData, TelegramID) VALUES 
            ('{datetime.date.today()}', '{telegramID}')""")
        con.commit()


def newAdmin(telegramID):
    if not cur.execute(f"""SELECT TelegramID FROM Admins WHERE TelegramID = '{telegramID}'""").fetchone():
        cur.execute(f"""INSERT INTO Admins (Name, TelegramID) VALUES 
            ('{telegramID}', '{telegramID}')""")
        con.commit()


def deleteUser(telegramID):
    cur.execute(f"""DELETE FROM interns WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getExp(telegramID):
    return cur.execute(f"""SELECT exp FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()[0]


def check_for_win(telegramID):
    prize_list = {"first": ["Стикер"], "second": ["ручка"], "third": ["яхта"]}
    quantity_for_first = 15
    quantity_for_second = 30
    quantity_for_third = 45
    if getExp(telegramID) > quantity_for_first:
        return prize_list["first"][randint(0, len(prize_list["first"]) - 1)]

    elif getExp(telegramID) > quantity_for_second:
        return prize_list["second"][randint(0, len(prize_list["second"]) - 1)]

    elif getExp(telegramID) > quantity_for_third:
        return prize_list["third"][randint(0, len(prize_list["third"]) - 1)]
    else:
        return None


def getCurrentDate():
    return datetime.datetime.now().date()

def check_for_data(telegramID):
    data = datetime.datetime.strptime(getData(telegramID), "%Y-%m-%d")
    current_date = datetime.datetime.today()
    # dif = current_date - data
    dif = 180 - (current_date - data).days
    return dif
    # возможно, это понадобится позже, но я пока что закомментирую это
    # if dif == 7:
    #     pass
    # elif dif == 14:
    #     pass
    # elif dif == 30:
    #     pass


def getData(telegramID):
    return cur.execute(f"""SELECT comingData FROM interns WHERE TelegramID = '{telegramID}'""").fetchone()[0]


def if_user_exist(telegramID):
    return bool(cur.execute(f"""SELECT TelegramID FROM interns WHERE TelegramID = '{telegramID}'""").fetchone())


def if_user_admin(telegramID):
    admin_list = [x[0] for x in cur.execute(f"""SELECT TelegramID FROM admins""").fetchall()]
    return str(telegramID) in admin_list

def getAdminList():
    return [x[0] for x in cur.execute(f"""SELECT TelegramID FROM admins""").fetchall()]

def appendQueue(telegramID):
    cur.execute(f"""INSERT INTO queue (TelegramID) VALUES ('{telegramID}')""")
    con.commit()


def appendChatActive(intern, Admin):
    cur.execute(f"""INSERT INTO activeChat (idIntern, idAdmin) VALUES ('{intern}', '{Admin}')""")
    con.commit()


def deleteChatActive(TelegramID):
    cur.execute(f"""DELETE FROM activeChat WHERE idIntern = {TelegramID} OR idAdmin = {TelegramID}""")
    con.commit()


def isChatActive(TelegramID):
    for s in cur.execute(f"""SELECT idIntern, idAdmin FROM activeChat""").fetchall():
        if s[0] == str(TelegramID) or s[1] == str(TelegramID):
            return True
    return False


def getIDinterlocutor(telegramID):
    chat = cur.execute(
        f"""SELECT idIntern, idAdmin FROM activeCHAT WHERE idIntern = '{telegramID}' or idAdmin ='{telegramID}'""").fetchone()
    if chat:
        if str(telegramID) == chat[0]:
            return int(chat[1])
        else:
            return int(chat[0])
    return telegramID


def deleteQueue(telegramID):
    cur.execute(f"""DELETE FROM queue WHERE TelegramID = '{telegramID}'""")
    con.commit()


def getQueue():
    return cur.execute(f"""SELECT TelegramID FROM queue""").fetchall()


def getTasks(telegramID):
    return cur.execute(f"""SELECT * FROM tasks WHERE id = {telegramID}""").fetchall()


def addTask(telegramID, newTask):
    cur.execute(f"""UPDATE interns set task = '{newTask}' WHERE TelegramID = '{telegramID}'""")
    con.commit()
    return "Задание обновлено"


# TODO: Подумать, как реализовать добавление очков
def addPoints(telegramID):
    pass

