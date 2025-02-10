from telebot import types

main_keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard_user = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel = types.ReplyKeyboardMarkup(resize_keyboard=True)

button_ask_question = types.KeyboardButton("❓️Задать вопрос")
button_my_questions = types.KeyboardButton("📬Мои вопросы")
button_spravka = types.KeyboardButton("🔍Частые вопросы")
button_info = types.KeyboardButton("📖Справочник")
button_admin_panel = types.KeyboardButton("🔑Админ панель")
button_questions = types.KeyboardButton(text='Вопросыℹ️')
button_home = types.KeyboardButton(text='🏠На главную')

main_keyboard_user.add(button_info, button_spravka)
main_keyboard_user.add(button_ask_question, button_my_questions)

main_keyboard_admin.add(button_info, button_spravka)
main_keyboard_admin.add(button_ask_question, button_my_questions)
main_keyboard_admin.add(button_admin_panel)

admin_panel.add(button_questions, button_home)