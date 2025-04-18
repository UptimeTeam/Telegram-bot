from telebot import types

main_keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard_user = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
faq_keyboard = types.InlineKeyboardMarkup()
spr_keyboard = types.InlineKeyboardMarkup()
kb_home = types.ReplyKeyboardMarkup(resize_keyboard=True)

button_ask_question = types.KeyboardButton("❓️Задать вопрос")
button_my_questions = types.KeyboardButton("📬Мои вопросы")
button_spravka = types.KeyboardButton("🔍Частые вопросы")
button_info = types.KeyboardButton("📖Справочник")
button_admin_panel = types.KeyboardButton("🔑Админ панель")
button_questions = types.KeyboardButton(text='Вопросыℹ️')
button_home = types.KeyboardButton(text='🏠На главную')

main_keyboard_user.add(button_info, button_spravka)
#main_keyboard_user.add(button_ask_question, button_my_questions)

main_keyboard_admin.add(button_info, button_spravka)
#main_keyboard_admin.add(button_ask_question, button_my_questions)
main_keyboard_admin.add(button_admin_panel)

admin_panel.add(button_questions, button_home)

kb_home.add(button_home)

key_1 = types.InlineKeyboardButton(text='Учебный процесс', callback_data='process')
faq_keyboard.add(key_1)
key_2 = types.InlineKeyboardButton(text='Документы и доступ', callback_data='document')
faq_keyboard.add(key_2)
key_3 = types.InlineKeyboardButton(text='Распределение и группы', callback_data='raspredelenie')
faq_keyboard.add(key_3)
key_4 = types.InlineKeyboardButton(text='Общежитие и корпуса', callback_data='obshaga')
faq_keyboard.add(key_4)
key_5 = types.InlineKeyboardButton(text='Стипендии', callback_data='stipa')
faq_keyboard.add(key_5)
key_6 = types.InlineKeyboardButton(text='Практика и воинский учет', callback_data='practikaandvoin')
faq_keyboard.add(key_6)
key_7 = types.InlineKeyboardButton(text='Отсутствие на учебе', callback_data='otsytstvie')
faq_keyboard.add(key_7)
key_8 = types.InlineKeyboardButton(text='Заочная форма обучения', callback_data='zaoch')
faq_keyboard.add(key_8)
key_9 = types.InlineKeyboardButton(text='Магистратура', callback_data='magistr')
faq_keyboard.add(key_9)
key_10 = types.InlineKeyboardButton(text='Распределение на профили', callback_data='specialties')
faq_keyboard.add(key_10)

spr_key_1 = types.InlineKeyboardButton(text='Центр медицинского обеспечения', callback_data='medicina')
spr_keyboard.add(spr_key_1)
spr_key_2 = types.InlineKeyboardButton(text='Библиотечно-издательский комплекс', callback_data='library')
spr_keyboard.add(spr_key_2)
spr_key_3 = types.InlineKeyboardButton(text='Общежития', callback_data='dormitory')
spr_keyboard.add(spr_key_3)
spr_key_4 = types.InlineKeyboardButton(text='ВШЦТ', callback_data='institute')
spr_keyboard.add(spr_key_4)
spr_key_5 = types.InlineKeyboardButton(text='Приемная комиссия', callback_data='comission')
spr_keyboard.add(spr_key_5)
spr_key_6 = types.InlineKeyboardButton(text='Корпуса ТИУ', callback_data='corpusestyuiu')
spr_keyboard.add(spr_key_6)

satisfaction_keyboard = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='да', callback_data='satisfaction_yes')
key_no = types.InlineKeyboardButton(text='нет', callback_data='satisfaction_no')
satisfaction_keyboard.add(key_yes, key_no)