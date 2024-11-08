from telebot import types
import telebot

bot = telebot.TeleBot('7933512901:AAFgV8RvDQH7_0UEceoMDynmunZwBBTO_MM')

# вывод на команду старт
    

@bot.message_handler(commands=['start'])
def main(message):
    # создаем клавиатуруруру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_corpuses = types.KeyboardButton("🏢Корпуса ТИУ")
    button_ask_question = types.KeyboardButton("❓️Задать вопрос")
    button_spravka = types.KeyboardButton("Справка")
    keyboard.add(button_corpuses, button_ask_question, button_spravka)  # добавляем новые кнопки
    bot.send_message(message.chat.id, 'Привет!\n\n🤖 "Студенческий Помощник" — ваш надежный спутник в мире учебы! '
                     'Этот бот создан для того, чтобы облегчить жизнь студентам. Он быстро отвечает на часто задаваемые '
                     'вопросы о расписании, экзаменах, учебных материалах и студенческой жизни.\n\n'
                     '📚 Просто напишите свой вопрос, и получите мгновенный ответ! Будь то информация о дедлайнах, '
                     'советы по подготовке к экзаменам или ресурсы для изучения — наш бот всегда готов помочь.\n\n'
                     '🎓 Учитесь с умом и не тратьте время на поиски информации — доверьтесь "Студенческому Помощнику!"',
                     reply_markup=keyboard)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         "Привет, чем я могу тебе помочь?")
    elif message.text == "🏢Корпуса ТИУ":
        # отправляем изображение с корпусами
        with open('корпус.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    elif message.text == "Справка":
        # Пишем приветствие
        # bot.send_message(message.from_user.id, "Какую информацию вы хотите получить?")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого вопроса
        key_obshaga = types.InlineKeyboardButton(text='Общежитие', callback_data='spravka')
        # И добавляем кнопку на экран
        keyboard.add(key_obshaga)
        key_1 = types.InlineKeyboardButton(text='Получить студенческий билет, зачетную книжку, кампусную карту, сдать аттестат ', callback_data='spravka')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='Узнать свою группу', callback_data='spravka')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Как попасть в корпус', callback_data='spravka')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='PRE-курс', callback_data='spravka')
        keyboard.add(key_4)
        key_5 = types.InlineKeyboardButton(text='Личный кабинет ТИУ, Educon', callback_data='spravka')
        keyboard.add(key_5)
        key_6 = types.InlineKeyboardButton(text='Коммуникации (беседа ВК, ТГ)', callback_data='spravka')
        keyboard.add(key_6)
        key_7 = types.InlineKeyboardButton(text='Перевод, отчисление, восстановление, академический отпуск', callback_data='spravka')
        keyboard.add(key_7)
        key_8 = types.InlineKeyboardButton(text='Справки', callback_data='spravka')
        keyboard.add(key_8)
        key_9 = types.InlineKeyboardButton(text='Стипендия', callback_data='spravka')
        keyboard.add(key_9)
        key_10 = types.InlineKeyboardButton(text='Повышенная стипендия', callback_data='spravka')
        keyboard.add(key_10)
        key_11 = types.InlineKeyboardButton(text='Расписание ', callback_data='spravka')
        keyboard.add(key_11) 
         # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Какую информацию вы хотите получить?' ,reply_markup=keyboard)
    elif message.text == "❓️Задать вопрос":
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите ваш вопрос, и я постараюсь на него ответить.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Напиши привет или нажми на кнопку.")
    else:
        bot.send_message(message.from_user.id,
                         "Я тебя не понимаю. Напиши /help.")

# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)

###