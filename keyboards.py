from telebot import types

# All buttons
button_add_task = types.KeyboardButton("Додати завдання")
button_view_my_tasks = types.KeyboardButton("Переглянути мої завдання")
button_write_one_set = types.KeyboardButton("Записати сет")
button_records = types.KeyboardButton("Рекорди")

button_yes = types.KeyboardButton("Так")
button_no = types.KeyboardButton("Ні")

button_admin_add_exercise = types.KeyboardButton("Додати вправу")
button_admin_add_record_type = types.KeyboardButton("Додати тип рекорду")
button_admin_view_all_exercise = types.KeyboardButton("Переглянути всі вправи")
button_admin_view_all_record_type = types.KeyboardButton("Переглянути всі типи рекорду")
button_admin_remove_exercise = types.KeyboardButton("Видалити вправу")
button_admin_remove_record_type = types.KeyboardButton("Видалити тип рекорду")

button_come_back = types.KeyboardButton("Назад")

button_view_my_records = types.KeyboardButton("Переглянути мої рекорди")
button_write_my_record = types.KeyboardButton("Записати новий рекорд")
button_view_records_others_user = types.KeyboardButton("Переглянути рекорди інших")

# Main
keyboard_main = types.ReplyKeyboardMarkup(True, row_width=2)
keyboard_main.add(button_add_task, button_view_my_tasks, button_write_one_set, button_records)

# Admin panel
keyboard_admin_panel = types.ReplyKeyboardMarkup(True, row_width=2)
keyboard_admin_panel.add(button_admin_add_exercise, button_admin_add_record_type, button_admin_view_all_exercise, button_admin_view_all_record_type, button_admin_remove_exercise, button_admin_remove_record_type)

# Records
keyboard_records = types.ReplyKeyboardMarkup(True, row_width=2)
keyboard_records.add(button_view_my_records, button_write_my_record, button_view_records_others_user, button_come_back)

# Only come back
keyboard_only_come_back = types.ReplyKeyboardMarkup(True)
keyboard_only_come_back.add(button_come_back)

# Yes or no
keyboard_yes_or_no = types.ReplyKeyboardMarkup(True)
keyboard_yes_or_no.add(button_yes, button_no)

keyboard_remove = types.ReplyKeyboardRemove()
