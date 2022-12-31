import time
import re
import telebot
import database_interaction
from datetime import date
from connect_to_database import connection
from data import TOKEN_TELEGRAM_BOT
from keyboards import *


bot_database = database_interaction.Bot_functions()
bot = telebot.TeleBot(TOKEN_TELEGRAM_BOT)



interface_name = ''

def view_all_users(message):
    try:
        all_username_list = bot_database.get_all_users()

        all_username_message = '\n'.join(all_username_list)

        bot.send_message(message.chat.id, all_username_message)
    except:
        bot.send_message(message.chat.id, "Немає жодного запису")

def view_all_exercise(message):
    try:
        all_exercise_list = bot_database.get_all_exercise()

        all_exercise_message = '\n'.join(all_exercise_list)

        bot.send_message(message.chat.id, all_exercise_message)
    except:
        bot.send_message(message.chat.id, "Немає жодного запису")

def view_all_record_type(message):
    try:
        all_record_type_list = bot_database.get_all_record_type()

        all_record_type_message = '\n'.join(all_record_type_list)

        bot.send_message(message.chat.id, all_record_type_message)
    except:
        bot.send_message(message.chat.id, "Немає жодного запису")

def view_my_tasks(message, date):
    global interface_name

    id_today = bot_database.get_id_today(date, message.from_user.id)

    if id_today is None:
        bot.send_message(message.chat.id, "На цю дату немає жодного запису")
    else:
        message_from_user_list = []

        all_records_from_need = bot_database.get_all_table_need_where_id_today(id_today)
        all_records_from_done =  bot_database.get_all_table_done_where_id_today(id_today)

        all_exercise = bot_database.get_all_exercise()

        for exercise in all_exercise:
            if exercise in all_records_from_need:
                exercise_need = all_records_from_need[f'{exercise}']
            else:
                exercise_need = 0
            if exercise in all_records_from_done:
                exercise_done = all_records_from_done[f'{exercise}']
            else:
                exercise_done = 0

            message_from_user_list.append(f'{exercise}  -  {exercise_need} / {exercise_done}')
        message_from_user =  '\n'.join(message_from_user_list)
        bot.send_message(message.chat.id, f"Вправа - потрібно / зроблено\n\n{message_from_user}", reply_markup=keyboard_main)

    bot.send_message(message.chat.id, "Повернення в меню", reply_markup=keyboard_main)
    interface_name = 'main'



def view_my_records_where_exercise(message):
    exercise_name_for_record = message.text
    records = bot_database.get_all_records_from_user_where_exercise(exercise_name_for_record, message.from_user.id)

    for record in records:
        record_message = '\n'.join(record)
        bot.send_message(message.chat.id, record_message, reply_markup=keyboard_main)

def view_records_user_where_exercise(message ,exercise, username):
    user_id = bot_database.get_user_id(username)

    records = bot_database.get_all_records_from_user_where_exercise(exercise, user_id)

    for record in records:
        record_message = '\n'.join(record)
        bot.send_message(message.chat.id, record_message, reply_markup=keyboard_main)


def exercise_is_available(message):
    exercise_available = bot_database.is_available('exercise', 'name', repr(f'{message.text}'))
    if exercise_available:
        return True
    else:
        return False

def user_is_available(message):
    user_available = bot_database.is_available('user', 'username', repr(f'{message.text}'))
    if user_available:
        return True
    else:
        return False

def record_type_is_available(message):
    record_type_available = bot_database.is_available('record_type', 'name', repr(f'{message.text}'))
    if record_type_available:
        return True
    else:
        return False


@bot.message_handler(commands=['admin'])
def admin(message):
    global interface_name
    bot.send_message(message.chat.id, "Для використання фунуцій адміністратора введи пароль")
    interface_name = 'admin_enter_password'

@bot.message_handler(func=lambda message: interface_name == 'admin_enter_password')
def admin_enter_password(message):
    global interface_name
    password = "AdminArtem"

    if message.text == password:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Вітаю в панелі адміністратора!", reply_markup=keyboard_admin_panel)
        interface_name = 'admin_panel'
    else:
        bot.send_message(message.chat.id, "Неправильний пароль, спробуйте ще раз")

# add exercise
@bot.message_handler(func=lambda message: message.text == button_admin_add_exercise.text and interface_name == 'admin_panel')
def admin_add_exercise(message):
    global interface_name
    bot.send_message(message.chat.id, "Введи назву нової вправи", reply_markup=keyboard_remove)
    interface_name = 'add_exercise_to_database'

@bot.message_handler(func=lambda message: interface_name == 'add_exercise_to_database')
def add_exercise_to_database(message):
    global interface_name
    exercise_available = bot_database.is_available('exercise', 'name', repr(f'{message.text}'))
    if not exercise_available:
        bot_database.add_exercise(message.text)
        bot.send_message(message.chat.id, f'Вправа "{message.text}" успішно додана', reply_markup=keyboard_admin_panel)
        interface_name = 'admin_panel'
    else:
        bot.send_message(message.chat.id, "Така вправа вже є, повтори спробу")

# view all exercise
@bot.message_handler(func=lambda message: message.text == button_admin_view_all_exercise.text and interface_name == 'admin_panel')
def admin_view_all_exercise(message):
    view_all_exercise(message)

# add record type
@bot.message_handler(func=lambda message: message.text == button_admin_add_record_type.text and interface_name == 'admin_panel')
def admin_add_record_type(message):
    global interface_name
    bot.send_message(message.chat.id, "Введи назву нового типу рекорду", reply_markup=keyboard_remove)
    interface_name = 'add_record_type_to_database'

@bot.message_handler(func=lambda message: interface_name == 'add_record_type_to_database')
def add_record_type_to_database(message):
    global interface_name
    record_type_available = bot_database.is_available('record_type', 'name', repr(f'{message.text}'))
    if not record_type_available:
        bot_database.add_record_type(message.text)
        bot.send_message(message.chat.id, f'Тип рекорду "{message.text}" успішно доданий', reply_markup=keyboard_admin_panel)
        interface_name = 'admin_panel'
    else:
        bot.send_message(message.chat.id, "Такий тип рекорду вже є, повтори спробу")

# view all record type
@bot.message_handler(func=lambda message: message.text == button_admin_view_all_record_type.text and interface_name == 'admin_panel')
def admin_view_all_record_type(message):
    view_all_record_type(message)

# remove exercise
@bot.message_handler(func=lambda message: message.text == button_admin_remove_exercise.text and interface_name == 'admin_panel')
def admin_remove_exercise(message):
    global interface_name
    bot.send_message(message.chat.id, "Введи назву вправи яку хочеш видалити", reply_markup=keyboard_remove)
    interface_name = 'remove_exercise_from_database'

@bot.message_handler(func=lambda message: interface_name == 'remove_exercise_from_database')
def remove_exercise_from_database(message):
    global interface_name
    exercise_available = bot_database.is_available('exercise', 'name', repr(f'{message.text}'))
    if exercise_available:
        bot_database.remove_exercise(message.text)
        bot.send_message(message.chat.id, f'Вправа "{message.text}" успішно видалена', reply_markup=keyboard_admin_panel)
        interface_name = 'admin_panel'
    else:
        bot.send_message(message.chat.id, "Такої вправи немає, повтори спробу")


# remove record type
@bot.message_handler(func=lambda message: message.text == button_admin_remove_record_type.text and interface_name == 'admin_panel')
def admin_remove_record_type(message):
    global interface_name
    bot.send_message(message.chat.id, "Введи назву типу рекорду яку хочеш видалити", reply_markup=keyboard_remove)
    interface_name = 'remove_record_type_from_database'

@bot.message_handler(func=lambda message: interface_name == 'remove_record_type_from_database')
def remove_record_type_from_database(message):
    record_type_available = bot_database.is_available('record_type', 'name', repr(f'{message.text}'))
    if record_type_available:
        global interface_name
        bot_database.remove_record_type(message.text)
        bot.send_message(message.chat.id, f'Тип рекорду "{message.text}" успішно видалений', reply_markup=keyboard_admin_panel)
        interface_name = 'admin_panel'
    else:
        bot.send_message(message.chat.id, "Такого типу рекорду немає, повтори спробу")





@bot.message_handler(commands=['start'])
def start(message):
    global interface_name

    telegram_user_id = message.from_user.id
    username = bot_database.get_username_user(telegram_user_id)

    if username is not None:
        bot.send_message(message.chat.id, f"З поверненням {username}!\nНагадаю тобі що з допомогою цього бота, ти зможеш записувати свої спортивні досягнення та спостерігати за досягненнями друзів.", reply_markup=keyboard_main)
        interface_name = "main"
    else:
        bot.send_message(message.chat.id, "Привіт! \nЗ допомогою цього бота, ти зможеш записувати свої спортивні досягнення та спостерігати за досягненнями друзів.")
        bot.send_message(message.chat.id, "Будь ласка, введи своє ігрове ім'я")

        interface_name = 'registration'

@bot.message_handler(func=lambda message: interface_name == 'registration')
def registration(message):
    global interface_name

    if re.search("\W", message.text) is None and len(message.text) <= 45:

        user_id = message.from_user.id
        user_mame = message.text

        bot.send_message(message.chat.id, f"Створено нового користувача з іменем {user_mame}", reply_markup=keyboard_main)
        interface_name = 'main'
        bot_database.create_new_user(user_id, user_mame)
    else:
        bot.send_message(message.chat.id, "Ви ввели некоректне ігрове ім'я, будь ласка повторіть спробу")





@bot.message_handler(func=lambda message: message.text == button_records.text and interface_name == 'main')
def records(message):
    global interface_name

    bot.send_message(message.chat.id, "Тут ти можеш стежити за своїми рекордами та рекордами інших", reply_markup=keyboard_records)
    interface_name = 'records'

# comeback to main
@bot.message_handler(func=lambda message: message.text == button_come_back.text and interface_name == 'records')
def comeback_to_main(message):
    global interface_name

    bot.send_message(message.chat.id, "Повернення до меню", reply_markup=keyboard_main)
    interface_name = 'main'

# view my record
@bot.message_handler(func=lambda message: message.text == button_view_my_records.text and interface_name == 'records')
def view_my_records_input_exercise(message):
    global interface_name

    bot.send_message(message.chat.id, "Введи назву вправи", reply_markup=keyboard_remove)
    view_all_exercise(message)
    interface_name = 'view_my_records_exercise_is_available'

@bot.message_handler(func=lambda message: interface_name == 'view_my_records_exercise_is_available')
def view_my_records_exercise_is_available(message):
    global interface_name

    if exercise_is_available(message):
        view_my_records_where_exercise(message)
        interface_name = 'main'
    else:
        bot.send_message(message.chat.id, "Такої вправи немає, повтори спробу")

# view records others user
view_records_others_user_data = []
@bot.message_handler(func=lambda message: message.text == button_view_records_others_user.text and interface_name == 'records')
def view_records_others_user(message):
    global interface_name
    global  view_records_others_user_data

    view_records_others_user_data = []

    bot.send_message(message.chat.id, "Введи назву вправи", reply_markup=keyboard_remove)
    view_all_exercise(message)
    interface_name = 'view_records_others_user_exercise_is_available'

@bot.message_handler(func=lambda message: interface_name == 'view_records_others_user_exercise_is_available')
def view_records_others_user_exercise_is_available(message):
    global interface_name

    if exercise_is_available(message):
        view_records_others_user_data.append(message.text)
        bot.send_message(message.chat.id, "Введи ім'я користувача, рекорди якого хочеш переглянути")
        view_all_users(message)
        interface_name = 'view_records_others_user_username_is_available'
    else:
        bot.send_message(message.chat.id, "Такої вправи немає, повтори спробу")

@bot.message_handler(func=lambda message: interface_name == 'view_records_others_user_username_is_available')
def view_records_others_user_username_is_available(message):
    global interface_name

    if user_is_available(message):
        view_records_others_user_data.append(message.text)
        print(view_records_others_user_data)
        view_records_user_where_exercise(message, *tuple(view_records_others_user_data))
        interface_name = 'main'
    else:
        bot.send_message(message.chat.id, "Такого користувача немає, повтори спробу")

# write my record
write_my_record_data = []
@bot.message_handler(func=lambda message: (message.text == button_write_my_record.text and interface_name == 'records')  or (message.text == button_yes.text and interface_name == 'write_my_record_input_new_data'))
def write_my_record_input_date(message):
    global interface_name
    global write_my_record_data

    write_my_record_data = []

    bot.send_message(message.chat.id, "Введи дату поставлення рекорду")
    bot.send_message(message.chat.id, "Формат дати - рік/місяць/день\nНаприклад: 2022-12-15", reply_markup=keyboard_remove)
    interface_name = 'write_my_record_date_is_valid'

@bot.message_handler(func=lambda message: interface_name == 'write_my_record_date_is_valid')
def write_my_record_date_is_valid(message):
    global interface_name
    global write_my_record_data

    try:
        time.strptime(message.text, '%Y-%m-%d')
        write_my_record_data.append(message.text)
        bot.send_message(message.chat.id ,"Введи назву вправи")
        view_all_exercise(message)
        interface_name = 'write_my_record_input_exercise'
    except:
        bot.send_message(message.chat.id, "Введена некоректна дата, повтори спробу")

@bot.message_handler(func=lambda message: interface_name == 'write_my_record_input_exercise')
def write_my_record_input_exercise(message):
    global interface_name
    global write_my_record_data

    if exercise_is_available(message):
        write_my_record_data.append(message.text)
        bot.send_message(message.chat.id, "Введи кількість повторювань")
        interface_name = 'write_my_record_input_repetitions'
    else:
        bot.send_message(message.chat.id, "Такої вправи немає, повтори спробу")

@bot.message_handler(func=lambda message: interface_name == 'write_my_record_input_repetitions')
def write_my_record_input_repetitions(message):
    global interface_name
    global write_my_record_data

    try:
        write_my_record_data.append(int(message.text))
        bot.send_message(message.chat.id, "Введи тип рекорду")
        view_all_record_type(message)
        interface_name = 'write_my_record_input_type_name'
    except:
        bot.send_message(message.chat.id, "Введено некоректне значення, повтори спробу")

@bot.message_handler(func=lambda message: interface_name == 'write_my_record_input_type_name')
def write_my_record_input_type_name(message):
    global interface_name
    global write_my_record_data

    if record_type_is_available(message):
        write_my_record_data.append(message.text)
        bot.send_message(message.chat.id, f"Дата - {write_my_record_data[0]}\nВправа - {write_my_record_data[1]}\nКількість повторювань - {write_my_record_data[2]}\nТип рекорду - {write_my_record_data[3]}")
        bot.send_message(message.chat.id, "Всі дані записано правильно?", reply_markup=keyboard_yes_or_no)
        interface_name = "write_my_record_data_is_valid"
    else:
        bot.send_message(message.chat.id, "Такого типу рекорду немає, повтори спробу")

@bot.message_handler(func=lambda message: message.text == button_yes.text and interface_name == 'write_my_record_data_is_valid')
def write_my_record_data_is_valid_yes(message):
    global interface_name
    global write_my_record_data

    write_my_record_data.append(message.from_user.id)
    bot_database.add_record(*tuple(write_my_record_data))
    bot.send_message(message.chat.id, "Рекорд успішно додано", reply_markup=keyboard_main)
    interface_name = 'main'

@bot.message_handler(func=lambda message: message.text == button_no.text and interface_name == 'write_my_record_data_is_valid')
def write_my_record_data_is_valid_no(message):
    global interface_name

    bot.send_message(message.chat.id, "Бажаєш заново заповнити дані?")
    interface_name = 'write_my_record_input_new_data'

@bot.message_handler(func=lambda message: message.text == button_no.text and interface_name == 'write_my_record_input_new_data')
def write_my_record_input_new_data_no(message):
    global interface_name

    bot.send_message(message.chat.id, "Повернення в головне меню", reply_markup=keyboard_main)
    interface_name = 'main'



# view my tasks
view_my_tasks_date = ''
@bot.message_handler(func=lambda message: message.text == button_view_my_tasks.text and interface_name == 'main')
def view_my_tasks_input_date(message):
    global interface_name

    bot.send_message(message.chat.id, "Введи дату за якою бажаєш переглянути завдання")
    bot.send_message(message.chat.id, "Формат дати - рік/місяць/день\nНаприклад: 2022-12-15", reply_markup=keyboard_remove)
    interface_name = 'view_my_tasks_date_is_valid'

@bot.message_handler(func=lambda message: interface_name == 'view_my_tasks_date_is_valid')
def view_my_tasks_date_is_valid(message):
    global interface_name
    global view_my_tasks_date

    try:
        time.strptime(message.text, '%Y-%m-%d')
        view_my_tasks_date = message.text
        view_my_tasks(message, view_my_tasks_date)
        interface_name = 'main'
    except:
        bot.send_message(message.chat.id, "Введена некоректна дата, повтори спробу")



# add task
add_task_data_l = []
@bot.message_handler(func=lambda message: (message.text == button_add_task.text and interface_name == 'main') or (message.text == button_yes.text and interface_name == 'add_task_input_new_data'))
def add_task_input_date(message):
    global interface_name

    bot.send_message(message.chat.id, "Введи дату на яку бажаєш записати завдання")
    bot.send_message(message.chat.id, "Формат дати - рік/місяць/день\nНаприклад: 2022-12-15", reply_markup=keyboard_remove)
    interface_name = 'add_task_date_is_valid'

@bot.message_handler(func=lambda message: interface_name == 'add_task_date_is_valid')
def add_task_date_is_valid(message):
    global interface_name
    global add_task_data_l

    try:
        time.strptime(message.text, '%Y-%m-%d')
        add_task_data_l.append(message.text)
        bot.send_message(message.chat.id ,"Введи назву вправи")
        view_all_exercise(message)
        interface_name = 'add_task_input_exercise'
    except:
        bot.send_message(message.chat.id, "Введена некоректна дата, повтори спробу")

@bot.message_handler(func=lambda message: interface_name == 'add_task_input_exercise')
def add_task_input_exercise(message):
    global interface_name
    global add_task_data_l

    if exercise_is_available(message):
        add_task_data_l.append(message.text)
        bot.send_message(message.chat.id, "Введи кількість повторювань")
        interface_name = 'add_task_input_repetitions'
    else:
        bot.send_message(message.chat.id, "Такої вправи немає, повтори спробу")

@bot.message_handler(func=lambda message: interface_name == 'add_task_input_repetitions')
def add_task_input_repetitions(message):
    global interface_name
    global add_task_data_l

    try:
        add_task_data_l.append(int(message.text))
        bot.send_message(message.chat.id, f"Дата - {add_task_data_l[0]}\nВправа - {add_task_data_l[1]}\nКількість повторювань - {add_task_data_l[2]}")
        bot.send_message(message.chat.id, "Всі дані записано правильно?", reply_markup=keyboard_yes_or_no)
        interface_name = "add_task_data_is_valid"
    except:
        bot.send_message(message.chat.id, "Введено некоректне значення, повтори спробу")

@bot.message_handler(func=lambda message: message.text == button_yes.text and interface_name == 'add_task_data_is_valid')
def add_task_data_is_valid_yes(message):
    global interface_name

    id_today = bot_database.get_id_today(add_task_data_l[0], message.from_user.id)
    if id_today is not None and (bot_database.is_available('need', 'today_id', id_today) and bot_database.is_available('need', 'exercise_name', repr(f'{add_task_data_l[1]}'))):
        bot.send_message(message.chat.id, "На цю дату завдання з такою вправою вже є", reply_markup=keyboard_main)
    else:
        bot_database.add_exercise_to_be_completed(message.from_user.id, add_task_data_l[0], add_task_data_l[1], add_task_data_l[2])
        bot.send_message(message.chat.id, "Завдання успішно додано", reply_markup=keyboard_main)

    interface_name = 'main'

@bot.message_handler(func=lambda message: message.text == button_no.text and interface_name == 'add_task_data_is_valid')
def add_task_data_is_valid_no(message):
    global interface_name

    bot.send_message(message.chat.id, "Бажаєш заново заповнити дані?")
    interface_name = 'add_task_input_new_data'

@bot.message_handler(func=lambda message: message.text == button_no.text and interface_name == 'add_task_input_new_data')
def add_task_input_new_data_no(message):
    global interface_name

    bot.send_message(message.chat.id, "Повернення в головне меню", reply_markup=keyboard_main)
    interface_name = 'main'





# add one set
add_one_set_data = []
@bot.message_handler(func=lambda message: (message.text == button_write_one_set.text and interface_name == 'main') or (message.text == button_yes.text and interface_name == 'add_one_set_input_new_data'))
def add_one_set_get_date(message):
    global interface_name
    global add_one_set_data

    add_one_set_data = []

    add_one_set_data.append(date.today())
    bot.send_message(message.chat.id ,"Введи назву вправи", reply_markup=keyboard_remove)
    view_all_exercise(message)
    interface_name = 'add_one_set_input_exercise'

@bot.message_handler(func=lambda message: interface_name == 'add_one_set_input_exercise')
def add_one_set_input_exercise(message):
    global interface_name
    global add_one_set_data

    if exercise_is_available(message):
        add_one_set_data.append(message.text)
        bot.send_message(message.chat.id, "Введи кількість повторювань")
        interface_name = 'add_one_set_input_repetitions'
    else:
        bot.send_message(message.chat.id, "Такої вправи немає, повтори спробу")

@bot.message_handler(func=lambda message: interface_name == 'add_one_set_input_repetitions')
def add_one_set_input_repetitions(message):
    global interface_name
    global add_one_set_data

    try:
        add_one_set_data.append(int(message.text))
        bot.send_message(message.chat.id, f"Вправа - {add_one_set_data[1]}\nКількість повторювань - {add_one_set_data[2]}")
        bot.send_message(message.chat.id, "Всі дані записано правильно?", reply_markup=keyboard_yes_or_no)
        interface_name = "add_one_set_data_is_valid"
    except:
        bot.send_message(message.chat.id, "Введено некоректне значення, повтори спробу")

@bot.message_handler(func=lambda message: message.text == button_yes.text and interface_name == 'add_one_set_data_is_valid')
def add_one_set_data_is_valid_yes(message):
    global interface_name

    bot_database.add_completed_exercise_in_one_set(message.from_user.id, *tuple(add_one_set_data))
    bot.send_message(message.chat.id, "Сет успішно додано", reply_markup=keyboard_main)
    interface_name = 'main'

@bot.message_handler(func=lambda message: message.text == button_no.text and interface_name == 'add_one_set_data_is_valid')
def add_one_set_data_is_valid_no(message):
    global interface_name

    bot.send_message(message.chat.id, "Бажаєш заново заповнити дані?")
    interface_name = 'add_one_set_input_new_data'

@bot.message_handler(func=lambda message: message.text == button_no.text and interface_name == 'add_one_set_input_new_data')
def add_one_set_input_new_data_no(message):
    global interface_name

    bot.send_message(message.chat.id, "Повернення в головне меню", reply_markup=keyboard_main)
    interface_name = 'main'



# bot.polling()





while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        bot.send_message(977081640, f'{e}')
        time.sleep(5)
