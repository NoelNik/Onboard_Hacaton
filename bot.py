import telebot
import time
from telebot import types
import DB
from config import TOKEN, PASSWORD

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['admin'])
def welcome(message):
    bot.send_message(message.chat.id, "Пожлалуйста, введите пароль: ")


@bot.message_handler(commands=['start'])
def welcome(message):
    DB.newUser(message.chat.id)
    bot.send_message(message.chat.id, "Привет! Я буду твоим помошником для удобной адаптации к новой рабочей среде")
    sti = open('media/stickers/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    menu(message)


# потом добавлю
@bot.message_handler(commands=['help'])
def help_me_pls(message):
    pass


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Рассказать про нашу компанию')
    item2 = types.KeyboardButton('Показать свой профиль')
    item3 = types.KeyboardButton('Связь с HR')
    item4 = types.KeyboardButton('Показать задания')
    item5 = types.KeyboardButton('Нормативные документы')

    markup.add(item1, item2, item3, item4, item5)
    if DB.if_user_admin(message.chat.id):
        markup.add(types.KeyboardButton('/menu_for_admin'))
    bot.send_message(message.chat.id, f'С чего вы хотите начать, {message.chat.first_name}',
                     reply_markup=markup)


@bot.message_handler(commands=['menu_for_admin'])
def menu_for_admin(message):
    if DB.if_user_admin(message.chat.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton('Добавить задания')
        item2 = types.KeyboardButton('Показать профиль работника')
        item3 = types.KeyboardButton('Открыть диолог со стажером')
        item4 = types.KeyboardButton('Удалить работника')

        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, f'С чего вы хотите начать, {message.chat.first_name}',
                         reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_echo(message):
    if message.text == 'Остановить диалог':
        bot.send_message(DB.getIDinterlocutor(message.chat.id), 'Диалог остановлен!')
        bot.send_message(message.chat.id, 'Диалог остановлен!')
        DB.deleteChatActive(message.chat.id)
        menu(message)
    elif DB.isChatActive(message.chat.id):
        bot.send_message(DB.getIDinterlocutor(message.chat.id), message.text)

    elif message.text == "Рассказать про нашу компанию":
        bot.send_message(message.chat.id, "Перейди по ссылке за всей нужной информацией :)")
        bot.send_message(message.chat.id, "https://disk.yandex.ru/d/SO7F8r0xI3DAsg")

    elif message.text == "Показать свой профиль":
        print(message.chat.id)
        bot.send_message(message.chat.id,
                         f"{message.chat.first_name}, вот сколько у тебя баллов: {DB.getExp(message.chat.id)}")

    elif message.text == "Связь с HR":
        chat_hr(message)

    elif message.text == 'Остановить поиск':
        DB.deleteQueue(message.chat.id)
        menu(message)

    elif message.text == "Показать задания":
        tasks = DB.getTasks(message.chat.id)
        if tasks:
            mes = f"Вот список твоих заданий:\n"
            for num, elem in enumerate(tasks, start=1):
                mes += f"{num}. {elem[1]}.  Кол-во баллов: {elem[2]},  дедлайн: {elem[3]}\n"
            bot.send_message(message.chat.id, mes)
        else:
            bot.send_message(message.chat.id, "У тебя нет текущих заданий, поздравляю!")

    elif message.text == "Нормативные документы":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("Для устройства на работу")
        item2 = types.KeyboardButton("Как уйти в отпуск?")
        item3 = types.KeyboardButton("Увольнение")
        item4 = types.KeyboardButton("/menu")
        markup.add(item1, item2, item3, item4)
        bot_msg = bot.send_message(message.chat.id, "Какой документ вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(bot_msg, get_documents)
    elif DB.if_user_admin(message.chat.id):
        if message.text == "Добавить задания":
            pass
        elif message.text == "Показать профиль работника":
            pass
        elif message.text == "Удалить работника":
            pass
        elif message.text == "Открыть диолог со стажером":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(types.KeyboardButton('Остановить диалог'))
            q = DB.getQueue()
            if q:
                DB.deleteQueue(q[0][0])
                DB.appendChatActive(q[0][0], message.chat.id)
                bot.send_message(message.chat.id, "Вы подключились к диалогу!", reply_markup=markup)
                bot.send_message(q[0][0], "Вы подключились к диалогу, задавайте вопросы!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Я не понял вашу команду")
            menu(message)
    else:
        bot.send_message(message.chat.id, "Я не понял вашу команду")
        menu(message)


def get_documents(message):
    if message.text == "Для устройства на работу":
        bot.send_message(message.chat.id, "тут будут доки для устройства на работу, когда Никита их допишет")
    elif message.text == "Как уйти в отпуск?":
        bot.send_message(message.chat.id, "тут будут доки для отпуска")
    elif message.text == "Увольнение":
        getAwayDoc = open('media/documents/Заявление об увольнении.docx', 'rb')
        bot.send_document(message.chat.id, getAwayDoc, caption="В таком случае, заполните это заявление")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял")
    menu(message)


def chat_hr(message):
    DB.appendQueue(message.chat.id)
    for i in DB.getAdminList():
        bot.send_message(int(i), f"Стажер встал в очередь! Сейчас в очереди {len(DB.getQueue())}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton('Остановить поиск'))
    bot.send_message(message.chat.id, "Подождите, пока сотрудник не присоединиться к чату", reply_markup=markup)


def complete_task(message):
    bot.send_message(message.chat.id, "Поздравляю, вы выполнили задание! Баллы добавлены в ваш профиль :)")


def start():
    bot.infinity_polling()
