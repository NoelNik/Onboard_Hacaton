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


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Рассказать про нашу компанию')
    item2 = types.KeyboardButton('Показать свой профиль')
    item3 = types.KeyboardButton('Связь с HR')
    item4 = types.KeyboardButton('Показать задания')
    item5 = types.KeyboardButton('Нормативные документы')

    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, f'С чего вы хотите начать, {message.chat.first_name}',
                     reply_markup=markup)


@bot.message_handler(commands=['menu_for_admin'])
def menu_for_admin(message):
    if DB.if_user_admin(message.chat.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton('Добавить задания')
        item2 = types.KeyboardButton('Показать профиль работника')
        item3 = types.KeyboardButton('рофлан')
        item4 = types.KeyboardButton('Удалить работника')

        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, f'С чего вы хотите начать, {message.chat.first_name}',
                        reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_echo(message):
    if message.text == PASSWORD:
        DB.newAdmin(message.chat.id)
        menu_for_admin(message)
    if DB.if_user_admin(message.chat.id):
        # TODO: Дорасписать функции для админки
        if message.text == "Добавить задания":
            pass
        elif message.text == "Показать профиль работника":
            pass
        elif message.text == "Удалить работника":
            pass
        elif message.text == "рофлан":
            bot.send_message(message.chat.id, "Начинается процесс удаления всего кода")
            for i in range(1, 11):
                time.sleep(1)
                bot.send_message(message.chat.id, f"До сноса всей программы осталось: {11 - i}")
            bot.stop_bot()


    if message.text == "Рассказать про нашу компанию":
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
        markup.add(item1, item2, item3)
        bot_msg = bot.send_message(message.chat.id, "Какой документ вас интересует?", reply_markup=markup)
        bot.register_next_step_handler(bot_msg, get_documents)


    else:
        item1 = types.KeyboardButton('/start')
        item2 = types.KeyboardButton('/help')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Я не понял вашу команду", reply_markup=markup)



def chat_hr(message):
    DB.appendQueue(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton('Остановить поиск'))
    bot.send_message(message.chat.id, "Подождите, пока сотрудник не присоединиться к чату", reply_markup=markup)


# TODO: придумать, как автоматизировать получение награды за выполнение задач!!!
def complete_task(message):
    bot.send_message(message.chat.id, "Поздравляю, вы выполнили задание! Баллы добавлены в ваш профиль :)")


def start():
    bot.infinity_polling()
