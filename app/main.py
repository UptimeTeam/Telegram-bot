from datetime import datetime
import sqlite3
from telebot import types
import telebot
from telebot.types import InputMediaPhoto


bot = telebot.TeleBot('7933512901:AAGiyFGykcactV1XrYq1hYTlnfaM2ai7JDQ')

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(telegram_id: int, first_name: str, username: str, created_at: datetime, updated_at: datetime):
	cursor.execute('REPLACE INTO users (telegram_id, first_name, username, created_at, updated_at) VALUES (?, ?, ?, ?, ?)', (telegram_id, first_name, username, created_at, updated_at))
	conn.commit()
def db_table_val_admin(admin_id: int, admin_name: str, created_at: datetime, updated_at: datetime):
	cursor.execute('REPLACE INTO admins (admin_id, admin_name, created_at, updated_at) VALUES (?, ?, ?, ?)', (admin_id, admin_name, created_at, updated_at))
	conn.commit()
def db_table_val_app(user_id: int, question: str, created_at: datetime, updated_at: datetime):
     cursor.execute('REPLACE INTO applications (user_id, question, created_at, updated_at) VALUES (?, ?, ?, ?)', (user_id, question, created_at, updated_at))
     conn.commit()

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_ask_question = types.KeyboardButton("❓️Задать вопрос")
button_spravka = types.KeyboardButton("🔍Часто задаваемые вопросы")
button_info = types.KeyboardButton("Справочник")
button_admin_panel = types.KeyboardButton("🔑Админ панель")
main_keyboard.add(button_info, button_ask_question, button_spravka)
    
@bot.message_handler(commands=['start'])
def main(message):
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    db_table_val(telegram_id=message.from_user.id,
                     first_name=message.from_user.first_name,
                     username=message.from_user.username,
                     created_at=datetime.now(),
                     updated_at=datetime.now())
    
    user_id = message.from_user.id
    if_admin = cursor.execute('SELECT EXISTS(SELECT * FROM admins where admin_id = ?)', (user_id, )).fetchone()[0]
    
    if if_admin:
        main_keyboard.add(button_info, button_ask_question, button_spravka, button_admin_panel)
    else: main_keyboard.add(button_info, button_ask_question, button_spravka)
    
    bot.send_message(message.chat.id, 'Привет!\n\n🤖 "Студенческий Помощник" — ваш надежный спутник в мире учебы! '
                     'Этот бот создан для того, чтобы облегчить жизнь студентам. Он быстро отвечает на часто задаваемые '
                     'вопросы о расписании, экзаменах, учебных материалах и студенческой жизни.\n\n'
                     '📚 Просто напишите свой вопрос, и получите мгновенный ответ! Будь то информация о дедлайнах, '
                     'советы по подготовке к экзаменам или ресурсы для изучения — наш бот всегда готов помочь.\n\n'
                     '🎓 Учитесь с умом и не тратьте время на поиски информации — доверьтесь "Студенческому Помощнику!"',
                     reply_markup=main_keyboard)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = message.from_user.id
    if_admin = cursor.execute('SELECT EXISTS(SELECT * FROM admins where admin_id = ?)', (user_id, )).fetchone()[0]
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id,
                         "Привет, %s! Чем я могу тебе помочь?" % message.from_user.first_name)
    
    elif message.text == "На главную🏠":
        global main_keyboard
        bot.send_message(message.from_user.id, text="Выберите раздел", reply_markup=main_keyboard)
    
    elif message.text == "uptimetop1":
        bot.send_message(message.from_user.id,
                         "Админ %s авторизован!" % message.from_user.first_name)
        adm_id = message.from_user.id
        adm_name = message.from_user.first_name
        crtd_at = datetime.now()
        upd_at = datetime.now()
        db_table_val_admin(admin_id=adm_id, admin_name=adm_name, created_at=crtd_at, updated_at=upd_at)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(button_info, button_ask_question, button_spravka, button_admin_panel)
        bot.send_message(message.from_user.id,
                         text="Привет, админ!", reply_markup=keyboard)
        
    elif message.text == "uptimenottop1":
        bot.send_message(message.from_user.id, "Админ %s уничтожен!" % message.from_user.first_name)
        cursor.execute(f'DELETE FROM admins WHERE admin_id = {message.from_user.id}')
        conn.commit()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(button_info, button_ask_question, button_spravka) 
        bot.send_message(message.from_user.id,
                         text="Пока!", reply_markup=keyboard)
    
    elif message.text == "🔑Админ панель" and if_admin:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = types.KeyboardButton(text='Вопросыℹ️')
        key_2 = types.KeyboardButton(text='На главную🏠')
        keyboard.add(key_1)
        keyboard.add(key_2)
        bot.send_message(message.from_user.id, text="Выберите раздел", reply_markup=keyboard)

    
    elif message.text == "Справочник":
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Центр медицинского обеспечения', callback_data='medicina')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='Библиотечно-издательский комплекс', callback_data='library')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Общежития', callback_data='dormitory')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='ВШЦТ', callback_data='institute')
        keyboard.add(key_4)
        key_5 = types.InlineKeyboardButton(text='Приемная комиссия', callback_data='commission')
        keyboard.add(key_5)
        key_6 = types.InlineKeyboardButton(text='Корпуса ТИУ', callback_data='corpusestyuiu')
        keyboard.add(key_6)
        bot.send_message(message.from_user.id, text='Какую информацию вы хотите получить?', reply_markup=keyboard)
    elif message.text == "🔍Часто задаваемые вопросы":
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого вопроса
        key_1 = types.InlineKeyboardButton(text='Распределение на профили', callback_data='raspredelenie')
        # И добавляем кнопку на экран
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='Номер группы', callback_data='nomer')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Информация о пропусках, картах, зачетках', callback_data='studbilet')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='Как попасть в корпус', callback_data='korpus')
        keyboard.add(key_4)
        key_5 = types.InlineKeyboardButton(text='Общежитие', callback_data='obshaga')
        keyboard.add(key_5)
        key_6 = types.InlineKeyboardButton(text='PRE-курс', callback_data='pre-kurs')
        keyboard.add(key_6)
        key_7 = types.InlineKeyboardButton(text='Личный кабинет ТИУ, Educon', callback_data='lk')
        keyboard.add(key_7)
        key_8 = types.InlineKeyboardButton(text='Сброс пароля zimbra', callback_data='zimbra')
        keyboard.add(key_8)
        key_9 = types.InlineKeyboardButton(text='Коммуникации (беседа ВК, ТГ)', callback_data='communication')
        keyboard.add(key_9)
        key_10 = types.InlineKeyboardButton(text='Перевод, отчисление, восстановление, академический отпуск', callback_data='poka')
        keyboard.add(key_10)
        key_11 = types.InlineKeyboardButton(text='Справки', callback_data='spravka')
        keyboard.add(key_11)
        
        key_12 = types.InlineKeyboardButton(text='Стипендия', callback_data='stipa')
        keyboard.add(key_12)
        key_13 = types.InlineKeyboardButton(text='Повышенная стипендия', callback_data='pgas')
        keyboard.add(key_13)
        key_14 = types.InlineKeyboardButton(text='Расписание', callback_data='raspisanie')
        keyboard.add(key_14) 
        key_15 = types.InlineKeyboardButton(text='Кураторы групп', callback_data='curators')
        keyboard.add(key_15) 
        key_16 = types.InlineKeyboardButton(text='Допуск к физкультуре', callback_data='PE')
        keyboard.add(key_16) 
        key_17 = types.InlineKeyboardButton(text='Не могу быть на учёбе (заболел, медкомиссия)', callback_data='absence')
        keyboard.add(key_17) 
        key_18 = types.InlineKeyboardButton(text='Календарный учебный график', callback_data='academic_calendar')
        keyboard.add(key_18) 
        key_19 = types.InlineKeyboardButton(text='Учебный план (какие будут дисциплины)', callback_data='curriculum')
        keyboard.add(key_19) 
        key_20 = types.InlineKeyboardButton(text='Элективы', callback_data='electives')
        keyboard.add(key_20) 
        key_21 = types.InlineKeyboardButton(text='Дирекция, территориальный отдел', callback_data='administration')
        keyboard.add(key_21) 
        key_22 = types.InlineKeyboardButton(text='Практика', callback_data='internship')
        keyboard.add(key_22) 
        key_23 = types.InlineKeyboardButton(text='Воинский учёт', callback_data='military_registration')
        keyboard.add(key_23)  
        bot.send_message(message.from_user.id, text='Какую информацию вы хотите получить?', reply_markup=keyboard)
    
    
    elif message.text == "Распределение на профили":
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Специальности', callback_data='specialties')
        keyboard.add(key_1)
        bot.send_message(message.from_user.id, text='Специальности', reply_markup=keyboard)
    elif message.text == "❓️Задать вопрос":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = types.KeyboardButton(text='На главную🏠')
        keyboard.add(key_1)
        bot.send_message(message.chat.id, "Пожалуйста, напишите ваш вопрос, и я передам его оператору.",reply_markup=keyboard)
        bot.register_next_step_handler(message, question_send)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет или нажми на кнопку.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
def question_send(message):
    question = message.text
    if question!="На главную🏠":
        db_table_val_app(user_id=message.from_user.id,
                     question=question,
                     created_at=datetime.now(),
                     updated_at=datetime.now())
        bot.send_message(message.from_user.id, text="Ваш вопрос принят!", reply_markup=main_keyboard)
    else: 
        bot.send_message(message.chat.id, "Выберите раздел",reply_markup=main_keyboard)

                
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    if call.data == 'medicina':
        bot.send_message(call.message.chat.id, "🏥 ЦЕНТР МЕДИЦИНСКОГО ОБЕСПЕЧЕНИЯ\n\n \nул. Володарского, 38, 3 этаж\n📞 7 (3452) 68 27 49 \nул. Нагорная, 6, 1 этаж, общежитие\n📞 7 (3452) 28 37 44 \nул. Киевская, 80, 1 этаж, общежитие \n\n⏰ Время работы: 08.00-15.00\n\n📎 https://www.tyuiu.ru/infrastruktura/centr-medicinskogo-obespeceniia/studentu")
    elif call.data == 'library':
        bot.send_message(call.message.chat.id, "📚 БИБЛИОТЕЧНО-ИЗДАТЕЛЬСКИЙ КОМПЛЕКС\n\n⏰ Режим работы комплекса: \nпн-пт: 8.00-18.00 \nсб.: 9.00-17.00,  \nвс.: выходной;  \nпоследний четверг месяца – санитарный день\n\nКонтакты:\nКаюкова Дарья Хрисановна \nДиректор \nБиблиотечно-издательского комплекса\nМельникайте, 72, каб. 42 \n📞 283070 \n✉️ kajukovadh@tyuiu.ru \n\nЕдиный телефон библиотечно-издательского комплекса: \n📞 7 (3452) 28 30 69\n\n📎https://www.tyuiu.ru/infrastruktura/bibliotecno-izdatelskii-kompleks/o-centre")
    elif call.data == 'dormitory':
        bot.send_message(call.message.chat.id, "🏢 ОБЩЕЖИТИЯ \n\nОБЩЕЖИТИЕ № 1 \nТип общежития: квартирный \nАдрес: г. Тюмень, ул. Мельникайте, 42 \nЗаведующая общежитием: Ковкова Татьяна Александровна \n📞 8 (3452) 28-35-71 \n\n ОБЩЕЖИТИЕ № 2 \nТип общежития: секционный повышенной комфортности. Мест для проживания  591. \nАдрес: г. Тюмень, ул. Нагорная, 6 \nЗаведующий общежитием: Киреев Александр Леонидович \nАдминистратор общежития: Вашлаева Татьяна Анатольевна \n📞 8 (3452) 28-37-24 \n\nОБЩЕЖИТИЕ № 2А \nТип общежития: секционный повышенной комфортности \nАдрес: г. Тюмень, ул. Нагорная, 6 \nЗаведующий общежитием: Кугаевская Евгения Викторовна \nАдминистратор общежития: Ващенко Оксана Леонидовна \n📞 8(3452) 28-34-29\n\nОБЩЕЖИТИЕ № 3 \nТип общежития: квартирный \nАдрес: г. Тюмень, ул. Нагорная, 34 \nЗаведующий общежитием: Ващенко Оксана Леонидовна \n📞 8 (3452) 28-37-29\n\nОБЩЕЖИТИЕ № 4 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. Мельникайте, 61 Б \nЗаведующая общежитием: Храмцова Татьяна Мануиловна \nАдминистратор общежития: Уртёнкова Татьяна Ниолаевна \n📞 8 (3452) 28-34-09\n\nОБЩЕЖИТИЕ № 5 \nТип общежития: секционный, частично повышенной комфортности. \nАдрес: г. Тюмень, ул. Мельникайте, 61 Б \nЗаведующая общежитием: Ступко Анна Валерьевна \nАдминистратор общежития: Дулдурова Анна Ивановна \n📞 8 (3452) 28-34-13 \n\nОБЩЕЖИТИЕ № 6 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. Мельникайте, 44 \nЗаведующая общежитием: Шафорост Лариса Геннадьевна \n📞 8 (3452) 28-35-68\n\nОБЩЕЖИТИЕ № 7 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. 50 лет ВЛКСМ, 45 А \nЗаведующий общежитием: Наливаева Наталья Владимировна \n📞 8 (3452) 28-34-15 \nВоспитатель: Абдуллина Елена Владимировна \nВоспитатель: Галингер Наталья Владимировна \nДежурный администратор (ночной воспитатель): Батырова Эльмира Хасановна \n\nОБЩЕЖИТИЕ № 8 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. 50 лет ВЛКСМ, 43 \nЗаведующий общежитием: Шлюева Ольга Александровна \n📞 8 (3452) 2834-14 \nВоспитатель: Бачалова Людмила Владимировна \nДежурные администраторы (ночные воспитатели):  \nКоролева Лариса Сергеевна \nБатырова Эльмира Хасановна\n\nОБЩЕЖИТИЕ № 9 \nТип общежития: 8-этажное блочное здание коридорного типа. \nАдрес: г. Тюмень, ул. Бабарынка, д. 20 Б \nЗаведующий общежитием: Бобенцева Людмила Николаевна \n📞 8 (3452) 28-30-67\n\nОБЩЕЖИТИЕ № 12 \nТип общежития: коридорный \nАдрес: г. Тюмень, ул. Киевская, 80 \nЗаведующий общежитием: Антипина Елена Владимировна \nВоспитатель: Гартунг Тамара Яковлевна \nДежурный администратор (ночной воспитатель):  \nБезрукова Наталья Васильевна \nЖуравлева Валентина Петровна \n📞 8 (3452) 53-85-56\n\nОБЩЕЖИТИЕ № 15 \nТип общежития: коридорный, повышенной комфортности \nАдрес: г. Тюмень, ул. Котовского, 54 А \nЗаведующий общежитием: Коробченко Елена Вафиковна \n📞 8 (3452) 28-34-10 \nАдминистратор общежития: Шония Манана Георгевна \nВоспитатели общежития: \nХалитова Татьяна Николаевна \nДежурные администраторы (ночные воспитатели): \nМеньщикова Ольга Николаеа\nШашкина Наталья Владимировна")
    elif call.data == 'institute':
        bot.send_message(call.message.chat.id, "💜 Высшая школа цифровых технологий \nул. Мельникайте 70\n📎 https://www.tyuiu.ru/obrazovanie/instituty/vyssaia-skola-cifrovyx-texnologii/ob-institute\n\n\nДИРЕКЦИЯ ИНСТИТУТА\nЧаусова Ангелина Сергеевна \n📞 7 (3452) 68 57 86 \n✉️ chausovaas@tyuiu.ru \nул. Мельникайте, 70, каб. 217\n\nОбращаться по вопросам, связанным с учебным процессом")
    elif call.data == 'comission':
        bot.send_message(call.message.chat.id, "📄 ПРИЕМНАЯ КОМИССИЯ \n\nг. Тюмень, ул. Республики, 47  \n📞 8 800 700 5771, 7 (3452) 68 57 66  \n\n✉️ priemcom@tyuiu.ru   \n\n⏰ понедельник — пятница: с 9:00 до 17:00  	\nсуббота, воскресенье: выходной")
    elif call.data == 'corpusestyuiu':
        # отправляем изображение с корпусами
        with open('файлы/корпус.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)


    elif call.data == 'raspredelenie':
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        button_raspredelen = types.InlineKeyboardButton("Изменить заявление", callback_data='raspredelen')
        button_specialty = types.InlineKeyboardButton("Специальность", callback_data='specialty')
        button_nomer = types.InlineKeyboardButton("Узнать номер группы", callback_data='nomer')
        button_statement = types.InlineKeyboardButton("Заполнение заявления", callback_data='statement')
        button_statement2 = types.InlineKeyboardButton("Заявление о распределении в конкрусе", callback_data='statement2')
        button_statement3 = types.InlineKeyboardButton("Чужое заявление", callback_data='statement3')
        button_statement4 = types.InlineKeyboardButton("Изменить заявление", callback_data='statement4')
        button_statement5 = types.InlineKeyboardButton("Когда писать заявление", callback_data='statement5')
        button_statement6 = types.InlineKeyboardButton("Заявление для целевого", callback_data='statement6')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        keyboard.add(button_raspredelen, button_specialty, button_nomer, button_statement, button_statement2, button_statement3, button_statement4, button_statement5, button_statement6, button_back)
        
        bot.edit_message_text("Выберите вопрос:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'raspredelen':
        bot.edit_message_text("Списки групп размещены/будут размещены в телеграмм-канале ВШЦТ.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'specialty':
        bot.edit_message_text("Информация для студентов ВШЦТ поступивших на 1 курс по направлению подготовки:\n\n🔄 09.03.01 Информатика и вычислительная техника (Автоматизированные системы обработки информации и управления)\n 🔄 09.03.01 Информатика и вычислительная техника (Информационная безопасность компьютерных систем и сетей)\n 🔄 09.03.02 Информационные системы и технологии (Информационные системы и технологии в геологии и нефтегазовой отрасли\n 🔄 09.03.02 Информационные системы и технологии (Искусственный интеллект и программирование)\n 🔄 09.03.02 Информационные системы и технологии (Интеллектуальные системы и технологии» Умный город»)\n 🔄 09.03.02 Информационные системы и технологии (Технология разработки и сопровождения программного продукта)\n \n Вы поступили в ВШЦТ в рамках многопрофильного конкурса, который предполагает процедуру распределения по профилям подготовки\n Вам необходимо выполнить следующее:\n 1️⃣Ознакомиться с Выпиской из инструкции \n 2️⃣Заполнить Заявление в двух вариантах заполнения ниже \n 🔄 вариант 1 распечатать заявление, подписать и принести 02.09.2024 на PRE-курс\n 🔄вариант 2 получить бланк заявления на PRE-курс, заполнить и подписать его на организационной встрече. \n \n Обращаем Ваше внимание, что в заявлении должны быть указаны все ШЕСТЬ профилей.\n Если Вы относитесь к категориям обучающихся, которые распределяются вне конкурса- необходимо принести с собой копии всех подтверждающих документов и приложить их к заявлению.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'nomer':
        bot.edit_message_text("Списки групп размещены/будут размещены в телеграмм-канале ВШЦТ", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'statement':
        bot.edit_message_text("Заявление по выбору профиля пишут поступившие на 1 курс только по направлению подготовки: 09.03.01 и 09.03.02", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'statement2':
        bot.edit_message_text("Вы поступили в ВШЦТ в рамках многопрофильного конкурса, который предполагает процедуру распределения по профилям подготовки. Вся информация и документы размещены в телеграмм-канале ВШЦТ", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'statement3':
        bot.edit_message_text("Нельзя подавать заявление за другого человека.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'statement4':
        bot.edit_message_text("К сожалению, если вы уже отдали заявление, то менять его нельзя.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'statement5':
        bot.edit_message_text("Заявление подаётся в определённые сроки, закреплённые нормативными документами. См. п.3 Выписки в телеграмм-канале ВШЦТ", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'statement6':
        bot.edit_message_text("Заявление пишется в обязательном порядке. Если Вы относитесь к категориям обучающихся, которые распределяются вне конкурса - необходимо принести с собой копии всех подтверждающих документов и приложить их к заявлению.\nСм. п.5.4 Выписки в телеграмм-канале ВШЦТ", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'back':
        get_text_messages(call.message)

    elif  call.data == 'nomer':
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        button_nom = types.InlineKeyboardButton("Узнать номер группы", callback_data='nom')
        button_cant = types.InlineKeyboardButton("Не могу найти себя в списке", callback_data='cant')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        keyboard.add(button_nom, button_cant, button_back)
        bot.edit_message_text("Выберите вопрос:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'nom':
        bot.send_message(call.message.chat.id, "Узнать номер группы вы можете в файле:")
        with open('ВШЦТ_списки_1 курс_распред.pdf', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
    elif call.data == 'cant':
        bot.send_message(call.message.chat.id, "Узнать номер группы вы можете в файле:")
        with open('ВШЦТ_списки_1 курс_распред.pdf', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
    elif call.data == 'back':
        get_text_messages(call.message)

    elif call.data == 'studbilet':
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        button_karta = types.InlineKeyboardButton("Пропускная карта", callback_data='karta')
        button_bilet = types.InlineKeyboardButton("Студенческий билет", callback_data='bilet')
        button_photo = types.InlineKeyboardButton("Фото для студенческого билета", callback_data='photo')
        button_kampus = types.InlineKeyboardButton("Отмена кампусной карты", callback_data='kampus')
        button_transport = types.InlineKeyboardButton("Транспротная карта", callback_data='transport')
        button_zachetki = types.InlineKeyboardButton("Зачетки", callback_data='zachetki')
        button_contact = types.InlineKeyboardButton("Контакты специалиста", callback_data='contact')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        keyboard.add(button_karta, button_bilet, button_photo, button_kampus, button_transport, button_zachetki, button_contact, button_back)
        bot.edit_message_text("Выберите вопрос:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'karta':
        bot.send_message(call.message.chat.id, "Расписание выдачи кампусных карт размещено/будет размещено в телеграмм-канале ВШЦТ")
    elif call.data == 'bilet':
        bot.send_message(call.message.chat.id, "До 30 августа необходимо принести 3 фото размером 3х4 для оформления студенческого и зачетки \n\nКуда нести? \nВ свой территориальный отдел \nул. Мельникайте д. 70, кабинет 204, 206 \n\nТакже на входе в каждый корпус будут стоять боксы, куда можно положить свои фото\n\n❗️Важно❗️\nНа Фотографиях с оборотной стороны надо написать свое ФИО полностью и название института")
    elif call.data == 'photo':
        bot.send_message(call.message.chat.id, "В территориальный отдел \n\nул. Мельникайте, д. 70, кабинет 204, 206 \n\nТакже на входе в каждый корпус будут стоять боксы, куда можно положить свои фото")
    elif call.data == 'kampus':
        bot.send_message(call.message.chat.id, "Необходимо обратиться к представителям банка.\nРасписание выдачи кампусных карт размещено/будет размещено в телеграмм-канале ВШЦТ")
    elif call.data == 'transport':
        bot.send_message(call.message.chat.id, "Транспортную карту необходимо активировать в Тюменской транспортной системе по адресу: ул. Котовского, д. 52  ")
    elif call.data == 'zachetki':
        bot.send_message(call.message.chat.id, "Надо сдавать зачетные книжки вашему специалисту территориального отдела.")
    elif call.data == 'contact':
        bot.send_message(call.message.chat.id, "Специалист Центра по работе с обучающимися - Скрипкина Татьяна Сергеевна, Республики, 47, каб. 217, номер:283651")
    elif call.data == 'back':
        get_text_messages(call.message)
    
    elif call.data == 'korpus':
        bot.send_message(call.message.chat.id, "Вся информация по входу в здания Университета размещена/будет размещена в телегам канале ВШЦТ.")
    elif call.data == 'obshaga':
        bot.send_message(call.message.chat.id, "Вся информация об общежитиях размещена на сайте ТИУ\nhttps://www.tyuiu.ru/infrastruktura/studenceskii-gorodok_/studgorodok")
    elif call.data == 'pre-kurs':
        bot.send_message(call.message.chat.id, "Вся информация по PREкурсу размещена/будет размещена в телегам канале ВШЦТ.")
    
    elif call.data == 'lk':
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        button_dostup = types.InlineKeyboardButton("Доступ в ЛК", callback_data='dostup')
        button_parol = types.InlineKeyboardButton("Слетел пароль", callback_data='parol')
        button_problem = types.InlineKeyboardButton("Проблемы со входом", callback_data='problem')
        button_zimbra = types.InlineKeyboardButton("Сброс пароля зимбра", callback_data='zimbra')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        keyboard.add(button_dostup, button_parol, button_problem, button_zimbra, button_back)
        bot.edit_message_text("Выберите вопрос:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'dostup':
        bot.send_message(call.message.chat.id, "Теперь расписание учебных занятий можно посмотреть в личном кабинете на платформе 'Мой ТИУ'. \nhttps://sso.tyuiu.ru \n\n❗️У вас может истечь срок действия пароля \nЕго нужно обновлять каждый год \nСоздайте новый через 'Забыл пароль' (Главное указывать почту/телефон которые вы предоставляли при поступлении)\n\nУ кого слетел пароль - инструкция 🫡⚠️\nhttps://t.me/iottyuiu22/102")
    elif call.data == 'parol':
        bot.send_message(call.message.chat.id, "У кого слетел пароль - инструкция 🫡⚠️\n\nhttps://t.me/iottyuiu22/102")
    elif call.data == 'problem':
        bot.send_message(call.message.chat.id, "Обратиться в дирекцию ВШЦТ \nпо адресу: ул. Мельникайте, д. 70, каб. 217\nпо тел.: 685786")
    elif call.data == 'zimbra':
        bot.send_message(call.message.chat.id,"Сброс пароля осуществляется пользователем самостоятельно, обновление происходит через сутки")
    elif call.data == 'back':
        get_text_messages(call.message)
    
    elif call.data == 'communication':
        bot.send_message(call.message.chat.id, "Чтобы найти беседу группы, необходимо написать вашему куратору.")
    elif call.data == 'poka':
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        button_otchislen = types.InlineKeyboardButton("Отчисление", callback_data='otchislen')
        button_dgroup = types.InlineKeyboardButton("Перевод в другую группу", callback_data='dgroup')
        button_armia = types.InlineKeyboardButton("Армия", callback_data='armia')
        button_dinstitute = types.InlineKeyboardButton("Перевод в другой институт", callback_data='dinstitute')
        button_academ = types.InlineKeyboardButton("Академический отпуск", callback_data='academ')
        button_back = types.InlineKeyboardButton("Назад", callback_data='back')
        keyboard.add(button_otchislen, button_dgroup, button_armia, button_dinstitute, button_academ, button_back)
        bot.edit_message_text("Выберите вопрос:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    elif call.data == 'otchislen':
        bot.send_message(call.message.chat.id, "Информацию по отчислению можно получить у специалиста территориального отдела.") 
    elif call.data == 'dgroup':
        bot.send_message(call.message.chat.id, "Перевод в другую группу осуществляется во время каникул при наличии свободных мест. Информацию по переводу можно получить специалиста территориального отдела.") 
    elif call.data == 'armia':
        bot.send_message(call.message.chat.id, "Информацию по академическому отпуску можно получить у специалиста территориального отдела.") 
    elif call.data == 'dinstitute':
        bot.send_message(call.message.chat.id, "Перевод возможен. Информацию можно получить у специалиста территориального отдела.") 
    elif call.data == 'academ':
        bot.send_message(call.message.chat.id, "Информацию по академическому отпуску можно получить у специалиста территориального отдела.") 
    elif call.data == 'back':
        get_text_messages(call.message)


    elif call.data == 'spravka':
        bot.send_message(call.message.chat.id, "Справки оформляются у вашего специалиста территориального отдела.") 
    
    elif call.data == 'stipa':
        bot.send_message(call.message.chat.id, "Согласно ПОЛОЖЕНИЯ о стипендиальном обеспечении и материальной поддержке обучающихся ТИУ: \n\n1️⃣ Стипендии, являясь денежными выплатами, назначаемыми обучающимся по очной форме обучения подразделяются на:\n- государственные академические стипендии студентам;\n- государственные социальные стипендии студентам;\n- стипендии Президента Российской Федерации;\n- стипендии Правительства Российской Федерации;\n- именные стипендии;\n- стипендии обучающимся, назначаемые юридическими лицами или физическими лицами, в том числе направившими их на обучение и др.\n\n💸 2️⃣ Обучающийся, которому назначается ГОСУДАРСТВЕННАЯ АКАДЕМИЧЕСКАЯ СТИПЕНДИЯ, должен соответствовать следующим требованиям:\n- отсутствие по итогам промежуточной аттестации оценки «удовлетворительно»;\n- отсутствие академической задолженности.\n\nЧтобы вам была начислена государственная академическая стипендия, необходимо в срок до 31.01.2025 подойти к своему специалисту территориального отдела (каб. 206, каб. 204) и отдать свою зачетную книжку для сверки оценок.")
    elif call.data == 'pgas':
        bot.send_message(call.message.chat.id, "ПОВЫШЕННАЯ ГОСУДАРСТВЕННАЯ АКАДЕМИЧЕСКАЯ СТИПЕНДИЯ (ПГАС) назначается:\n\n1) за достижения студента в учебной деятельност \n2) за достижения студента в научно-исследовательской деятельности\n3) за достижения студента в общественной деятельности\n4) за достижения студента в культурно-творческой деятельности\n5) за достижения студента в спортивной деятельности \n\nМинимальный и максимальный размер ПГАС указан в файле «Размер_стипендий_2023-24», пункты 8.1-8.10 Критерии назначения приведены в файле «ПГАС» -  читаем внимательно! \n\nДля назначения ПГАС необходимо заполнить формы (В ЭЛЕКТРОННОМ ВИДЕ, И РАСПЕЧАТАТЬ!! ОТ РУКИ НЕ ЗАПОЛНЯТЬ!), приведенные в файле «Формы представлений», предоставить в Дирекцию ВШЦТ (каб. 217) копии ВСЕХ подтверждающих документов.")
        with open('файлы/ПГАС.docx', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
        with open('файлы/формы_представлений_ПГАС.docx', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
        with open('файлы/Размер_стипендий_2023-2024.pdf', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
    elif call.data == 'raspisanie':
        bot.send_message(call.message.chat.id, "Расписание вы можете найти в личном кабинете сайта https://my.tyuiu.ru/ в разделе 'Расписание'.")
    elif call.data == 'curators':
        bot.send_message(call.message.chat.id, "Список кураторов групп...")
    elif call.data == 'PE':
        bot.send_message(call.message.chat.id, "Обучающиеся 1-3 курсов на начало учебного года обязаны предоставить медицинское заключение о допуске к занятиям по физической культуре и спорту, выполнению нормативов ГТО (Приложение1)  или заключения врачебной комиссии о принадлежности к физкультурной группе здоровья (Приложение2).Документы по установленной форме студент предоставляет в срок до 13 сентября преподавателю дисциплины 'Физическая культура и спорт'. В случает отсутствия медицинского заключения- студент до занятий не допускается, в результате чего автоматически возникает долг по дисциплине.")
        with open('файлы/Приложение1_Физ_ра.docx', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
        with open('файлы/Приложение2_Физ_ра.docx', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
    elif call.data == 'absence':
        bot.send_message(call.message.chat.id, "Если вы не можете быть на учёбе, пожалуйста, сообщите об этом своему куратору.")
    elif call.data == 'academic_calendar':
        caption = ("НАПОМИНАНИЕ ☑️ \n\n"
                "Как найти календарный учебный график (КУГ) на https://www.tyuiu.ru/ 👩‍💻 \n\n"
                "Смотри и сохраняй инструкцию😉 \n\n"
                "P.S. Как читать КУГ: \n\n"
                "1️⃣ Найди строку своего курса и направления подготовки \n\n"
                "2️⃣ Каждый столбец - шестидневная учебная неделя. Даты в заголовке таблицы стоят с учётом воскресенья, а самих клеток в столбце шесть, "
                "потому что воскресенье - выходной по умолчанию \n\n"
                "3️⃣ Находи в строке своего курса и направления столбец с необходимым обозначением (их расшифровка указана перед таблицей)")

        media = []
        for i in range(1, 7):
            if i == 1:
                # Первое фото с подписью
                media.append(InputMediaPhoto(open(f'файлы/УП{i}.png', 'rb'), caption=caption))
            else:
                media.append(InputMediaPhoto(open(f'файлы/academic_calendar{i}.png', 'rb')))
        bot.send_media_group(chat_id=call.message.chat.id, media=media)
    elif call.data == 'curriculum':
        caption = ("УЧЕБНЫЙ ПЛАН 🧐\n\n"
               "Посмотреть, по каким учебным дисциплинам у вас зачет, а по каким экзамен, увидеть дисциплины будущих семестров можно в учебном плане (УП).\n\n"
               "Это документ, который определяет перечень трудоемкости, последовательности и распределения по периодам обучения учебных предметов, курсов, дисциплин (модулей), практики, иных видов учебной деятельности и формы промежуточной аттестации обучающихся.\n\n"
               "Рассказываем, как его найти: смотри и сохраняй инструкцию 😉\n\n"
               "ВАЖНО:\n"
               "🔺 При поиске своего направления в таблице обрати внимание на форму обучения (очная) и уровень образования (бакалавриат / специалитет).\n"
               "🔺 В УП цифры, указанные в столбцах 'форма контроля', обозначают семестр, в котором они предусмотрены.\n\n"
               "Обозначения в УП:\n"
               "▪️КП - курсовой проект\n"
               "▪️КР - курсовая работа\n"
               "▪️ПОР - проектно-ориентированная работа\n\n"
               "Также вы можете посмотреть, какие формы занятий предусмотрены по каждой дисциплине:\n"
               "▪️Лек - лекция\n"
               "▪️Лаб - лабораторная\n"
               "▪️Пр - практика")
        media = []
        for i in range(1, 7):
            if i == 1:
                # Первое фото с подписью
                media.append(InputMediaPhoto(open(f'файлы/УП{i}.png', 'rb'), caption=caption))
            else:
                media.append(InputMediaPhoto(open(f'файлы/УП{i}.png', 'rb')))
        bot.send_media_group(chat_id=call.message.chat.id, media=media)
    elif call.data == 'electives':
        bot.send_message(call.message.chat.id, "Информация о элективах предоставляется на сайте университета.")
    elif call.data == 'administration':
        bot.send_message(call.message.chat.id, "Дирекция ВШЦТ \nМакарова Анна Сергеевна: ул. Мельникайте 70, ауд. 206 \nПочта: makarovaas@tyuiu.ru \nТелефон рабочий: (3452) 28-39-74 \n\nРяхина Юлия Юрьевна: ул. Мельникайте 70, ауд. 206 \nПочта: rjahinajj@tyuiu.ru \nТелефон рабочий: (3452) 28-39-74")
    elif call.data == 'internship':
        bot.send_message(call.message.chat.id, "Информация о практике доступна у вашего куратора.")
    elif call.data == 'military_registration':
        bot.send_message(call.message.chat.id, "Всем молодым людям  необходимо провести сверку документов воинского учета в отделе мобилизационной подготовки по адресу: ул. Володарского, 38 кабинет №110 с 9 сентября  по 13 сентября. При себе иметь паспорт, воинский документ (удостоверение гражданина подлежащего призыву на военную службу или военный билет), иногородние Свидетельство о временной регистрации (если имеется).Время работы отдела мобилизационной подготовки: пн.-четв. с 9:00 до 17:00, пятн. с 9:00 до 16:00. Обед с 13:00 до 14:00")

        
# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
