from telebot import types
import telebot
from telebot.types import InputMediaPhoto
import kb, texts
from db import get_db_connection
from psycopg2 import OperationalError

bot = telebot.TeleBot('7933512901:AAGiyFGykcactV1XrYq1hYTlnfaM2ai7JDQ')

conn = get_db_connection()
cursor = conn.cursor()


def db_table_val(telegram_id: int, first_name: str, username: str):
	cursor.execute('''
    INSERT INTO users (telegram_id, firstname, username) 
    VALUES (%s, %s, %s)
    ON CONFLICT (telegram_id) 
    DO UPDATE SET 
        firstname = EXCLUDED.firstname,
        username = EXCLUDED.username
''', (telegram_id, first_name, username))
	conn.commit()
def db_table_val_admin(admin_tg_id: int, admin_name: str, admin_username: str):
    cursor.execute('''INSERT INTO admins
    (admin_tg_id, admin_name, admin_username) 
    VALUES (%s, %s, %s)
    ON CONFLICT (admin_tg_id) 
    DO UPDATE SET 
        admin_name = EXCLUDED.admin_name,
        admin_username = EXCLUDED.admin_username
''', (admin_tg_id, admin_name, admin_username))
    conn.commit()
def db_table_val_app(user_id: int, username:str, question: str, answer: str, status:bool):
    cursor.execute('''INSERT INTO applications
    (telegram_id, username, question, answer, status) 
    VALUES (%s, %s, %s, %s, %s)
''', (user_id, username, question, answer, status))
    conn.commit()

questionnum = 1
myquestionnum = 1
user_id=1
    
@bot.message_handler(commands=['start'])
def main(message):
    global user_id
    user_id=message.from_user.id
    cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = %s)', (user_id,))
    if_exist = cursor.fetchone()[0]
    try:
        cursor.execute('SELECT EXISTS(SELECT 1 FROM admins WHERE admin_tg_id = %s)', (user_id,))
        if_admin = cursor.fetchone()[0]
        conn.commit()

    except OperationalError as e:
        print(f"Ошибка базы данных: {e}")
        conn.rollback()

    if not if_exist:
        db_table_val(telegram_id=message.from_user.id,
                     first_name=message.from_user.first_name,
                     username=message.from_user.username)
        
    if if_admin: bot.send_message(message.chat.id, texts.hello_admin, reply_markup=kb.main_keyboard_admin)
    else: bot.send_message(message.chat.id, texts.hello_user, reply_markup=kb.main_keyboard_user)



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    
    global user_id
    user_id = message.from_user.id
    try:
        cursor.execute('SELECT EXISTS(SELECT 1 FROM admins WHERE admin_tg_id = %s)', (user_id,))
        if_admin = cursor.fetchone()[0]
        conn.commit()

    except OperationalError as e:
        print(f"Ошибка базы данных: {e}")
        conn.rollback()
    
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, %s! Чем я могу тебе помочь?" % message.from_user.first_name)
    
    elif message.text == "🏠На главную":
        if if_admin: bot.send_message(message.chat.id, texts.home, reply_markup=kb.main_keyboard_admin)
        else: bot.send_message(message.chat.id, texts.home, reply_markup=kb.main_keyboard_user)
    
    elif message.text == "uptimetop1":
        cursor.execute('SELECT EXISTS(SELECT 1 FROM admins WHERE admin_tg_id = %s)', (user_id,))
        if_exist_admin = cursor.fetchone()[0]
        
        if if_exist_admin:
            bot.send_message(message.from_user.id, "С возвращением!", reply_markup=kb.main_keyboard_admin)
        else:
            admin_id = message.from_user.id
            admin_name = message.from_user.first_name
            admin_username = message.from_user.username
            db_table_val_admin(admin_tg_id=admin_id, admin_name=admin_name, admin_username=admin_username)
            bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup=kb.main_keyboard_admin)
        
    elif message.text == "uptimenottop1":
        cursor.execute(f'DELETE FROM admins WHERE admin_tg_id = {message.from_user.id}')
        conn.commit()
        bot.send_message(message.from_user.id, "Админ уничтожен!", reply_markup=kb.main_keyboard_user)
    
    elif message.text == "🔑Админ панель" and if_admin:
        bot.send_message(message.from_user.id, text="Выберите раздел", reply_markup=kb.admin_panel)
        
    elif message.text == "Вопросыℹ️" and if_admin:
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='⬅️', callback_data='previousq')
        key_2 = types.InlineKeyboardButton(text='Ответить', callback_data='answer_await')
        key_3 = types.InlineKeyboardButton(text='➡️', callback_data='nextq')
        keyboard.add(key_1, key_2, key_3) 
        
        try:
            cursor.execute('SELECT id FROM applications where status=False')
            questionnum = cursor.fetchone()[0]
            cursor.execute('SELECT username FROM applications where id=%s', (questionnum,))
            quser = cursor.fetchone()[0]
            cursor.execute('SELECT question FROM applications where id=%s', (questionnum,))
            qtext = cursor.fetchone()[0]
            bot.send_message(message.from_user.id, text=F"Вопрос #{questionnum} от @{quser}\n\n{qtext}", reply_markup=keyboard)
        except:
            bot.send_message(message.from_user.id, text="Все вопросы уже решены!", reply_markup=keyboard)

    
    elif message.text == "📬Мои вопросы":
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='⬅️', callback_data='previousmyq')
        key_3 = types.InlineKeyboardButton(text='➡️', callback_data='nextmyq')
        keyboard.add(key_1, key_3) 
        
        try:
            cursor.execute('SELECT question FROM applications where telegram_id=%s', (user_id,))
            myqtext = cursor.fetchone()[0]
            cursor.execute('SELECT id FROM applications where telegram_id=%s', (user_id,))
            myquestionnum = cursor.fetchone()[0]
            cursor.execute('SELECT answer FROM applications where telegram_id=%s', (user_id,))
            myquestionans = cursor.fetchone()[0]
            bot.send_message(message.from_user.id, text=F"Вопрос #{myquestionnum}\n\n{myqtext}\n\nОтвет: {myquestionans}", reply_markup=keyboard)
        except:
            bot.send_message(message.from_user.id, text="Вы пока не задали ни одного вопроса")

    elif message.text == "📖Справочник":
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Центр медицинского обеспечения', callback_data='medicina')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='Библиотечно-издательский комплекс', callback_data='library')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Общежития', callback_data='dormitory')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='ВШЦТ', callback_data='institute')
        keyboard.add(key_4)
        key_5 = types.InlineKeyboardButton(text='Приемная комиссия', callback_data='comission')
        keyboard.add(key_5)
        key_6 = types.InlineKeyboardButton(text='Корпуса ТИУ', callback_data='corpusestyuiu')
        keyboard.add(key_6)
        bot.send_message(message.from_user.id, text='Какую информацию вы хотите получить?', reply_markup=keyboard)
    elif message.text == "🔍Частые вопросы":
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
        key_24 = types.InlineKeyboardButton(text='Заочники', callback_data='zaoch')
        keyboard.add(key_24)
        key_25 = types.InlineKeyboardButton(text='Магистры', callback_data='magistr')
        keyboard.add(key_25)
        bot.send_message(message.from_user.id, text='Какую информацию вы хотите получить?', reply_markup=keyboard)
    
    
    elif message.text == "Распределение на профили":
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Специальности', callback_data='specialties')
        keyboard.add(key_1)
        bot.send_message(message.from_user.id, text='Специальности', reply_markup=keyboard)
    elif message.text == "❓️Задать вопрос":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = types.KeyboardButton(text='🏠На главную')
        keyboard.add(key_1)
        bot.send_message(message.chat.id, "Пожалуйста, напишите ваш вопрос, и я передам его оператору",reply_markup=keyboard)
        bot.register_next_step_handler(message, question_send)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет или нажми на кнопку.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
def question_send(message):
    global user_id
    try:
        cursor.execute('SELECT EXISTS(SELECT 1 FROM admins WHERE admin_tg_id = %s)', (user_id,))
        if_admin = cursor.fetchone()[0]
        conn.commit()

    except OperationalError as e:
        print(f"Ошибка базы данных: {e}")
        conn.rollback()
    user_id = message.from_user.id
    question = message.text
    if question!='🏠На главную':
        db_table_val_app(user_id=message.from_user.id,
                    username = message.from_user.username,
                    question=question,
                    answer="Пока на этот вопрос не ответили",
                    status = False)
        notify_admins(question, message.from_user.username)
        if if_admin: bot.send_message(message.chat.id, "Ваш вопрос принят!", reply_markup=kb.main_keyboard_admin)
        else: bot.send_message(message.chat.id, "Ваш вопрос принят!", reply_markup=kb.main_keyboard_user)
    else: 
        if if_admin: bot.send_message(message.chat.id, texts.home, reply_markup=kb.main_keyboard_admin)
        else: bot.send_message(message.chat.id, texts.home, reply_markup=kb.main_keyboard_user)

def notify_admins(question, username):
    cursor.execute("SELECT admin_tg_id FROM admins")
    admins = cursor.fetchone()
    if admins:
        message_text = f"\U0001F514 Новый вопрос от @{username}:\n{question}"
        for admin in admins:
            try:
                bot.send_message(admin, message_text)
            except Exception as e:
                print(f"Ошибка отправки уведомления администратору {admin}: {e}")

def answer_send(message):
    try:
        cursor.execute('SELECT EXISTS(SELECT 1 FROM admins WHERE admin_tg_id = %s)', (user_id,))
        if_admin = cursor.fetchone()[0]
        conn.commit()

    except OperationalError as e:
        print(f"Ошибка базы данных: {e}")
        conn.rollback()
    global questionnum
    answer = message.text
    if answer=='🏠На главную':
        if if_admin: bot.send_message(message.chat.id, texts.home, reply_markup=kb.main_keyboard_admin)
        else: bot.send_message(message.chat.id, texts.home, reply_markup=kb.main_keyboard_user)
        
    elif answer=='🔙Назад':
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='⬅️', callback_data='previousq')
        key_2 = types.InlineKeyboardButton(text='Ответить', callback_data='answer_await')
        key_3 = types.InlineKeyboardButton(text='➡️', callback_data='nextq')
        keyboard.add(key_1, key_2, key_3) 
        
        cursor.execute('SELECT question FROM applications where id=%s', (questionnum,))
        qtext = cursor.fetchone()[0]
        questionnum = questionnum
        cursor.execute('SELECT username FROM applications where id=%s', (questionnum,))
        quser = cursor.fetchone()[0]
        
        bot.send_message(message.from_user.id, text=F"Вопрос #{questionnum} от @{quser}\n\n{qtext}", reply_markup=keyboard)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = types.KeyboardButton(text='🏠На главную')
        key_2 = types.KeyboardButton(text='🔙Назад ')
        keyboard.add(key_1)
        keyboard.add(key_2)
        cursor.execute('UPDATE applications SET answer = %s WHERE id = %s', (answer, questionnum))
        conn.commit()
        cursor.execute('UPDATE applications SET status = %s WHERE id = %s', (True,questionnum))
        conn.commit()
        bot.send_message(message.from_user.id, text="Ответ отправлен!")

@bot.callback_query_handler(func=lambda call: call.data == 'directory')
def handle_directory(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    if call.message.message_id - 1 > 0:
        bot.delete_message(call.from_user.id, call.message.message_id - 1)
    keyboard = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text='Центр медицинского обеспечения', callback_data='medicina')
    keyboard.add(key_1)
    key_2 = types.InlineKeyboardButton(text='Библиотечно-издательский комплекс', callback_data='library')
    keyboard.add(key_2)
    key_3 = types.InlineKeyboardButton(text='Общежития', callback_data='dormitory')
    keyboard.add(key_3)
    key_4 = types.InlineKeyboardButton(text='ВШЦТ', callback_data='institute')
    keyboard.add(key_4)
    key_5 = types.InlineKeyboardButton(text='Приемная комиссия', callback_data='comission')
    keyboard.add(key_5)
    key_6 = types.InlineKeyboardButton(text='Корпуса ТИУ', callback_data='corpusestyuiu')
    keyboard.add(key_6)
    bot.send_message(call.from_user.id, text='Какую информацию вы хотите получить?', reply_markup=keyboard)
                
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global user_id
    global questionnum 
    global myquestionnum 
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    if call.data == 'medicina':
        keyboard = types.InlineKeyboardMarkup()
        key_back6 = types.InlineKeyboardButton(text='Назад', callback_data='directory')
        keyboard.add(key_back6)
        bot.send_message(call.message.chat.id, "🏥 ЦЕНТР МЕДИЦИНСКОГО ОБЕСПЕЧЕНИЯ\n\n \nул. Володарского, 38, 3 этаж\n📞 7 (3452) 68 27 49 \nул. Нагорная, 6, 1 этаж, общежитие\n📞 7 (3452) 28 37 44 \nул. Киевская, 80, 1 этаж, общежитие \n\n⏰ Время работы: 08.00-15.00\n\n📎 https://www.tyuiu.ru/infrastruktura/centr-medicinskogo-obespeceniia/studentu", reply_markup=keyboard)
    elif call.data == 'library':
        keyboard = types.InlineKeyboardMarkup()
        key_back7 = types.InlineKeyboardButton(text='Назад', callback_data='directory')
        keyboard.add(key_back7)
        bot.send_message(call.message.chat.id, "📚 БИБЛИОТЕЧНО-ИЗДАТЕЛЬСКИЙ КОМПЛЕКС\n\n⏰ Режим работы комплекса: \nпн-пт: 8.00-18.00 \nсб.: 9.00-17.00,  \nвс.: выходной;  \nпоследний четверг месяца – санитарный день\n\nКонтакты:\nКаюкова Дарья Хрисановна \nДиректор \nБиблиотечно-издательского комплекса\nМельникайте, 72, каб. 42 \n📞 283070 \n✉️ kajukovadh@tyuiu.ru \n\nЕдиный телефон библиотечно-издательского комплекса: \n📞 7 (3452) 28 30 69\n\n📎https://www.tyuiu.ru/infrastruktura/bibliotecno-izdatelskii-kompleks/o-centre", reply_markup=keyboard)
    elif call.data == 'dormitory':
        keyboard = types.InlineKeyboardMarkup()
        key_back6 = types.InlineKeyboardButton(text='Назад', callback_data='directory')
        keyboard.add(key_back6)
        bot.send_message(call.message.chat.id, "🏢 ОБЩЕЖИТИЯ \n\nОБЩЕЖИТИЕ № 1 \nТип общежития: квартирный \nАдрес: г. Тюмень, ул. Мельникайте, 42 \nЗаведующая общежитием: Ковкова Татьяна Александровна \n📞 8 (3452) 28-35-71 \n\n ОБЩЕЖИТИЕ № 2 \nТип общежития: секционный повышенной комфортности. Мест для проживания  591. \nАдрес: г. Тюмень, ул. Нагорная, 6 \nЗаведующий общежитием: Киреев Александр Леонидович \nАдминистратор общежития: Вашлаева Татьяна Анатольевна \n📞 8 (3452) 28-37-24 \n\nОБЩЕЖИТИЕ № 2А \nТип общежития: секционный повышенной комфортности \nАдрес: г. Тюмень, ул. Нагорная, 6 \nЗаведующий общежитием: Кугаевская Евгения Викторовна \nАдминистратор общежития: Ващенко Оксана Леонидовна \n📞 8(3452) 28-34-29\n\nОБЩЕЖИТИЕ № 3 \nТип общежития: квартирный \nАдрес: г. Тюмень, ул. Нагорная, 34 \nЗаведующий общежитием: Ващенко Оксана Леонидовна \n📞 8 (3452) 28-37-29\n\nОБЩЕЖИТИЕ № 4 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. Мельникайте, 61 Б \nЗаведующая общежитием: Храмцова Татьяна Мануиловна \nАдминистратор общежития: Уртёнкова Татьяна Ниолаевна \n📞 8 (3452) 28-34-09\n\nОБЩЕЖИТИЕ № 5 \nТип общежития: секционный, частично повышенной комфортности. \nАдрес: г. Тюмень, ул. Мельникайте, 61 Б \nЗаведующая общежитием: Ступко Анна Валерьевна \nАдминистратор общежития: Дулдурова Анна Ивановна \n📞 8 (3452) 28-34-13 \n\nОБЩЕЖИТИЕ № 6 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. Мельникайте, 44 \nЗаведующая общежитием: Шафорост Лариса Геннадьевна \n📞 8 (3452) 28-35-68\n\nОБЩЕЖИТИЕ № 7 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. 50 лет ВЛКСМ, 45 А \nЗаведующий общежитием: Наливаева Наталья Владимировна \n📞 8 (3452) 28-34-15 \nВоспитатель: Абдуллина Елена Владимировна \nВоспитатель: Галингер Наталья Владимировна \nДежурный администратор (ночной воспитатель): Батырова Эльмира Хасановна \n\nОБЩЕЖИТИЕ № 8 \nТип общежития: секционный \nАдрес: г. Тюмень, ул. 50 лет ВЛКСМ, 43 \nЗаведующий общежитием: Шлюева Ольга Александровна \n📞 8 (3452) 2834-14 \nВоспитатель: Бачалова Людмила Владимировна \nДежурные администраторы (ночные воспитатели):  \nКоролева Лариса Сергеевна \nБатырова Эльмира Хасановна\n\nОБЩЕЖИТИЕ № 9 \nТип общежития: 8-этажное блочное здание коридорного типа. \nАдрес: г. Тюмень, ул. Бабарынка, д. 20 Б \nЗаведующий общежитием: Бобенцева Людмила Николаевна \n📞 8 (3452) 28-30-67\n\nОБЩЕЖИТИЕ № 12 \nТип общежития: коридорный \nАдрес: г. Тюмень, ул. Киевская, 80 \nЗаведующий общежитием: Антипина Елена Владимировна \nВоспитатель: Гартунг Тамара Яковлевна \nДежурный администратор (ночной воспитатель):  \nБезрукова Наталья Васильевна \nЖуравлева Валентина Петровна \n📞 8 (3452) 53-85-56\n\nОБЩЕЖИТИЕ № 15 \nТип общежития: коридорный, повышенной комфортности \nАдрес: г. Тюмень, ул. Котовского, 54 А \nЗаведующий общежитием: Коробченко Елена Вафиковна \n📞 8 (3452) 28-34-10 \nАдминистратор общежития: Шония Манана Георгевна \nВоспитатели общежития: \nХалитова Татьяна Николаевна \nДежурные администраторы (ночные воспитатели): \nМеньщикова Ольга Николаеа\nШашкина Наталья Владимировна", reply_markup=keyboard)
    elif call.data == 'institute':
        keyboard = types.InlineKeyboardMarkup()
        key_back6 = types.InlineKeyboardButton(text='Назад', callback_data='directory')
        keyboard.add(key_back6)
        bot.send_message(call.message.chat.id, "💜 Высшая школа цифровых технологий \nул. Мельникайте 70\n📎 https://www.tyuiu.ru/obrazovanie/instituty/vyssaia-skola-cifrovyx-texnologii/ob-institute\n\n\nДИРЕКЦИЯ ИНСТИТУТА\nЧаусова Ангелина Сергеевна \n📞 7 (3452) 68 57 86 \n✉️ chausovaas@tyuiu.ru \nул. Мельникайте, 70, каб. 217\n\nОбращаться по вопросам, связанным с учебным процессом", reply_markup=keyboard)
    elif call.data == 'comission':
        keyboard = types.InlineKeyboardMarkup()
        key_back6 = types.InlineKeyboardButton(text='Назад', callback_data='directory')
        keyboard.add(key_back6)
        bot.send_message(call.message.chat.id, "📄 ПРИЕМНАЯ КОМИССИЯ \n\nг. Тюмень, ул. Республики, 47  \n📞 8 800 700 5771, 7 (3452) 68 57 66  \n\n✉️ priemcom@tyuiu.ru   \n\n⏰ понедельник — пятница: с 9:00 до 17:00  	\nсуббота, воскресенье: выходной", reply_markup=keyboard)
    elif call.data == 'corpusestyuiu':
        # отправляем изображение с корпусами
        keyboard = types.InlineKeyboardMarkup()
        key_back6 = types.InlineKeyboardButton(text='Назад', callback_data='directory')
        keyboard.add(key_back6)
        with open('файлы/корпус.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, reply_markup=keyboard)
            
    elif call.data == 'previousq':
        
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='⬅️', callback_data='previousq')
        key_2 = types.InlineKeyboardButton(text='Ответить', callback_data='answer_await')
        key_3 = types.InlineKeyboardButton(text='➡️', callback_data='nextq')
        keyboard.add(key_1, key_2, key_3)       
        try: 
            cursor.execute('SELECT id FROM applications where status=False AND id<%s', (questionnum,))
            questionnum = cursor.fetchone()[0]
        except:
            cursor.execute('SELECT id FROM applications where status=False')
            questionnum = cursor.fetchone()[0]
        cursor.execute('SELECT question FROM applications where id=%s', (questionnum,))
        qtext = cursor.fetchone()[0]
        cursor.execute('SELECT username FROM applications where id=%s', (questionnum,))
        quser = cursor.fetchone()[0]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=F"Вопрос #{questionnum} от @{quser}\n\n{qtext}", reply_markup=keyboard)    
            
    elif call.data == 'answer_await':        
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_1 = types.KeyboardButton(text='🏠На главную')
        key_2 = types.KeyboardButton(text='🔙Назад ')
        keyboard.add(key_1)
        keyboard.add(key_2)
        bot.send_message(call.message.chat.id, "Напишите ответ на этот вопрос",reply_markup=keyboard)
        bot.register_next_step_handler(call.message, answer_send)
            
    elif call.data == 'nextq':        
        
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='⬅️', callback_data='previousq')
        key_2 = types.InlineKeyboardButton(text='Ответить', callback_data='answer_await')
        key_3 = types.InlineKeyboardButton(text='➡️', callback_data='nextq')
        keyboard.add(key_1, key_2, key_3)    
        try:
            cursor.execute('SELECT id FROM applications where status=False AND id>%s', (questionnum,))
            questionnum = cursor.fetchone()[0]
        except:
            cursor.execute('SELECT id FROM applications where status=False')
            questionnum = cursor.fetchone()[0]
        cursor.execute('SELECT question FROM applications where id=%s', (questionnum,))
        qtext = cursor.fetchone()[0]
        cursor.execute('SELECT username FROM applications where id=%s', (questionnum,))
        quser = cursor.fetchone()[0]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=F"Вопрос #{questionnum} от @{quser}\n\n{qtext}", reply_markup=keyboard)
    
    elif call.data == 'previousmyq':        
        
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='⬅️', callback_data='previousmyq')
        key_3 = types.InlineKeyboardButton(text='➡️', callback_data='nextmyq')
        keyboard.add(key_1, key_3)    
        try: 
            cursor.execute('SELECT id FROM applications where telegram_id=%s AND id<%s', (user_id,questionnum,))
            myquestionnum = cursor.fetchone()[0]
        except: 
            cursor.execute('SELECT id FROM applications where telegram_id=%s', (user_id,))
            myquestionnum = cursor.fetchone()[0]
        cursor.execute('SELECT question FROM applications where id=%s', (myquestionnum,))
        myqtext = cursor.fetchone()[0]
        cursor.execute('SELECT answer FROM applications where id=%s', (myquestionnum,))
        myquestionans = cursor.fetchone()[0]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=F"Вопрос #{myquestionnum}\n\n{myqtext}\n\nОтвет: {myquestionans}", reply_markup=keyboard)
    
    elif call.data == 'nextmyq':        
         
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='⬅️', callback_data='previousmyq')
        key_3 = types.InlineKeyboardButton(text='➡️', callback_data='nextmyq')
        keyboard.add(key_1, key_3)    
        try: 
            cursor.execute('SELECT id FROM applications where telegram_id=%s AND id>%s', (user_id,questionnum,))
            myquestionnum = cursor.fetchone()[0]
        except:
            cursor.execute('SELECT id FROM applications where telegram_id=%s', (user_id,))
            myquestionnum = cursor.fetchone()[0]
        cursor.execute('SELECT question FROM applications where id=%s', (myquestionnum,))
        myqtext = cursor.fetchone()[0]
        cursor.execute('SELECT answer FROM applications where id=%s', (myquestionnum,))
        myquestionans = cursor.fetchone()[0]
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=F"Вопрос #{myquestionnum}\n\n{myqtext}\n\nОтвет: {myquestionans}", reply_markup=keyboard)

    elif call.data == 'raspredelenie':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
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
        keyboard = types.InlineKeyboardMarkup
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
        message_text = (
            "<b>👤Кураторы групп</b>\n\n"
            "✔️<b>Информация по кураторам и списки групп</b> размещена/будет размещена в телеграмм канале ВШЦТ.\n\n"
            "✔️<b>Контактные данные куратора</b> размещены/будут размещены в телеграмм канале ВШЦТ."
        )
        bot.send_message(call.message.chat.id, message_text, parse_mode='HTML')


    elif call.data == 'PE':
        message_text = (
            "<b>🏃‍♀️‍➡️Допуск к физкультуре</b>\n\n"
            "✔️Обучающиеся 1-3 курсов на начало учебного года <b>обязаны</b> предоставить медицинское заключение о допуске к занятиям по физической культуре и спорту, выполнению нормативов ГТО (Приложение1) или заключения врачебной комиссии о принадлежности к физкультурной группе здоровья (Приложение2).\n\n"
            "✔️<b>Документы по установленной форме студент предоставляет в срок до 13 сентября</b> преподавателю дисциплины 'Физическая культура и спорт'.\n\n"
            "✔️<b>В случае отсутствия медицинского заключения</b> - студент до занятий не допускается, в результате чего автоматически возникает долг по дисциплине.\n\n"
            "❗️<b>Занятия в тренажёрном зале никак не пересекаются с обязательным посещением физкультуры</b>"
         )
    
    
        bot.send_message(call.message.chat.id, message_text, parse_mode='HTML')
    
        with open('файлы/Приложение1_Физ_ра.docx', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
        with open('файлы/Приложение2_Физ_ра.docx', 'rb') as document:
            bot.send_document(call.message.chat.id, document)



    elif call.data == 'absence':
        message_text = (
            "<b>🤒НЕ могу быть на учебе:</b>\n\n"
            "1️⃣<b>В случае болезни</b> необходимо довести информацию до старосты своей группы.\n\n"
            "2️⃣<b>Отсутствие на занятиях по болезни должно быть подтверждено медицинской справкой из медицинского учреждения.</b> "
            "По выходу с больничного подойти к преподавателю и объяснить причину отсутствия."
        )
    
        bot.send_message(call.message.chat.id, message_text, parse_mode='HTML')

    
    elif call.data == 'academic_calendar':
        caption = (
            "📅 Календарный учебный график \n\n"
            "✔️Календарный учебный график (КУГ) - документ, определяющий последовательность и чередование обучения (урочной и внеурочной деятельности), "
            "сроки промежуточной аттестации, плановых перерывов (каникулы и праздничные дни) при получении образования. \n\n"
            "✔️Актуальные даты указаны в документе на сайте ТИУ: "
            "https://tyuiu.ru/obrazovanie/instituty/vyssaia-skola-cifrovyx-texnologii/studentam"
        )

        media = []
        for i in range(1, 7):
            if i == 1:
            # Первое фото с подписью
                media.append(InputMediaPhoto(open(f'файлы/УП{i}.png', 'rb'), caption=caption))
            else:
                media.append(InputMediaPhoto(open(f'файлы/academic_calendar{i}.png', 'rb')))
    
        bot.send_media_group(chat_id=call.message.chat.id, media=media)


    elif call.data == 'curriculum':
        caption = ( 
                   "📚Учебный план (какие будут дисциплины)\n\n"
                    "✔️Ознакомиться с учебным планом можно на сайте ТИУ: "
                "https://tyuiu.ru/sveden/education/eduop/\n\n")
        media = []
        for i in range(1, 7):
            if i == 1:
                # Первое фото с подписью
                media.append(InputMediaPhoto(open(f'файлы/УП{i}.png', 'rb'), caption=caption))
            else:
                media.append(InputMediaPhoto(open(f'файлы/УП{i}.png', 'rb')))
        bot.send_media_group(chat_id=call.message.chat.id, media=media)
    elif call.data == 'electives':
        caption = (
            "<b>👥Элективы</b>\n\n"
            "Информацию можно узнать у тьютора образовательных траекторий."
        )
    
        bot.send_message(call.message.chat.id, caption, parse_mode='HTML')

    elif call.data == 'administration':
        caption = (
            "<b>👩🏼‍💻Дирекция, территориальный отдел</b>\n\n"
            "🕖Часы работы\n"
            "Пн-пт: 9:00-12:00 13:00-17:00\n"
            "Сб: 9:00-15:00\n\n"
            "Режим работы методистов:\n"
            "👤Макарова Анна Сергеевна - ул. Мельникайте 70, ауд. 206\n"
            "Почта: makarovaas@tyuiu.ru\n"
            "Телефон рабочий: (3452) 28-39-74\n\n"
            "👤Ряхина Юлия Юрьевна - ул. Мельникайте 70, ауд. 206\n"
            "Почта: rjahinajj@tyuiu.ru\n"
            "Телефон рабочий: (3452) 28-39-74"
        )
        
        bot.send_message(call.message.chat.id, caption, parse_mode='HTML')

    elif call.data == 'internship':
        caption = (
            "<b>📑Практика</b>\n\n"
            "По вопросам организации практической подготовки <b>обращаться к ответственному за организацию практики от вашей кафедры или руководителю практики</b>"
        )
        
        bot.send_message(call.message.chat.id, caption, parse_mode='HTML')

    elif call.data == 'military_registration':
        bot.send_message(call.message.chat.id, "Всем молодым людям  необходимо провести сверку документов воинского учета в отделе мобилизационной подготовки по адресу: ул. Володарского, 38 кабинет №110 с 9 сентября  по 13 сентября. При себе иметь паспорт, воинский документ (удостоверение гражданина подлежащего призыву на военную службу или военный билет), иногородние Свидетельство о временной регистрации (если имеется).Время работы отдела мобилизационной подготовки: пн.-четв. с 9:00 до 17:00, пятн. с 9:00 до 16:00. Обед с 13:00 до 14:00")
        
    elif call.data == 'zaoch':
        caption = (
            "<b>📚Заочники</b>\n\n"
            "✔️Вся информация придёт Вам на почту, указанную при поступлении.\n\n"
            "✔️Актуальные даты указаны в календарном учебном графике на сайте ТИУ: "
            "https://tyuiu.ru/obrazovanie/instituty/vyssaia-skola-cifrovyx-texnologii/\n\n"
            "✔️Информацию о переводе можно получить у специалиста территориального отдела. "
            "Кампусные карты выдаются только для студентов очной формы обучения."
        )
        
        bot.send_message(call.message.chat.id, caption, parse_mode='HTML')

    
    elif call.data == 'magistr':
        caption = (
            "<b>🧑🏻‍🎓Магистры</b>\n\n"
            "✔️Вся актуальная информация будет размещена в телеграмм-канале ВШЦТ. "
            "На электронную почту, которую вы указывали при поступлении, придет информация по доступу на электронный ресурс Эдукон.\n\n"
            "✔️По почте России придет справка-вызов. Сессия начнется 9 января. Расписание появляется на сайте за неделю до сессии.\n\n"
            "✔️Актуальные даты указаны в календарном учебном графике на сайте ТИУ: "
            "https://tyuiu.ru/obrazovanie/instituty/vyssaia-skola-cifrovyx-texnologii/studentam"
        )
        
        bot.send_message(call.message.chat.id, caption, parse_mode='HTML')



        
# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
