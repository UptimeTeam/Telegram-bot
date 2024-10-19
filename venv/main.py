from telebot import types
import telebot

bot = telebot.TeleBot('7933512901:AAFgV8RvDQH7_0UEceoMDynmunZwBBTO_MM')

# вывод на команду старт


@bot.message_handler(commands=['start'])
def main(message):
    # создаем клавиатуруруру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_corpuses = types.KeyboardButton("🏢Корпуса ТИУ")
    button_ask_question = types.KeyboardButton(
        "❓️Задать вопрос")
    markup.add(button_corpuses, button_ask_question)  # добавляем новые кнопки
    bot.send_message(message.chat.id, 'Привет!\n\n🤖 "Студенческий Помощник" — ваш надежный спутник в мире учебы! '
                     'Этот бот создан для того, чтобы облегчить жизнь студентам. Он быстро отвечает на часто задаваемые '
                     'вопросы о расписании, экзаменах, учебных материалах и студенческой жизни.\n\n'
                     '📚 Просто напишите свой вопрос, и получите мгновенный ответ! Будь то информация о дедлайнах, '
                     'советы по подготовке к экзаменам или ресурсы для изучения — наш бот всегда готов помочь.\n\n'
                     '🎓 Учитесь с умом и не тратьте время на поиски информации — доверьтесь "Студенческому Помощнику!"',
                     reply_markup=markup)

# крч этих штук можно много создавать и они все отвечают за какие-то команды
# @bot.message_handler(commands=['help'])
# def main(message):
#     bot.send_message(message.chat.id, 'Информация о помощи')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         "Привет, чем я могу тебе помочь?")
    elif message.text == "🏢Корпуса ТИУ":
        # отправляем изображение с корпусами
        with open('корпус.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    elif message.text == "❓️Задать вопрос":
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите ваш вопрос, и я постараюсь на него ответить.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         "Напиши привет или нажми на кнопку.")
    else:
        bot.send_message(message.from_user.id,
                         "Я тебя не понимаю. Напиши /help.")


# чтобы ботик не останавливался, без этого сообщение не выводит
bot.polling(none_stop=True)
