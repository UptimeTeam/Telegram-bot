import logging
from contextlib import asynccontextmanager
from app.bot.create_bot import bot, dp, stop_bot, start_bot
from app.bot.user_router import user_router
from app.config import settings
from aiogram.types import Update
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

<<<<<<< Updated upstream

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(user_router)
    await start_bot()
    webhook_url = settings.get_webhook_url()
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    logging.info(f"Webhook set to {webhook_url}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)
=======
def db_table_val_user(telegram_id: int, first_name: str, username: str, created_at: datetime, updated_at: datetime):
	cursor.execute('REPLACE INTO users (telegram_id, first_name, username, created_at, updated_at) VALUES (?, ?, ?, ?, ?)', (telegram_id, first_name, username, created_at, updated_at))
	conn.commit()
def db_table_val_admin(admin_id: int, admin_name: str, created_at: datetime, updated_at: datetime):
	cursor.execute('REPLACE INTO admins (admin_id, admin_name, created_at, updated_at) VALUES (?, ?, ?, ?)', (admin_id, admin_name, created_at, updated_at))
	conn.commit()

# вывод на команду старт
    
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_ask_question = types.KeyboardButton("❓️Задать вопрос")
button_spravka = types.KeyboardButton("🔍Часто задаваемые вопросы")
button_info = types.KeyboardButton("Справочник")
button_admin_panel = types.KeyboardButton("🔑Админ панель")    

@bot.message_handler(commands=['start'])
def main(message):
    # создаем клавиатуруруру
    if_admin = cursor.execute('SELECT EXISTS(SELECT * FROM admins where admin_id = ?)', (message.from_user.id, )).fetchone()[0]
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
    if_admin = cursor.execute('SELECT EXISTS(SELECT * FROM admins where admin_id = ?)', (message.from_user.id, )).fetchone()[0]
    if message.text == "Привет":
        bot.send_message(message.from_user.id,
                         "Привет, %s! Чем я могу тебе помочь?" % message.from_user.first_name)
        
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        crtd_at = datetime.now()
        username = message.from_user.username
        upd_at = datetime.now()
        db_table_val_user(telegram_id=us_id, first_name=us_name, username=username, created_at=crtd_at, updated_at=upd_at)
        
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
        keyboard = types.ReplyKeyboardMarkup()
        key_1 = types.KeyboardButton(text='Вопросы')
        keyboard.add(key_1)
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
        # отправляем изображение с корпусами
        bot.send_message(message.from_user.id, text='Какую информацию вы хотите получить?', reply_markup=keyboard)
        
    elif message.text == "🔍Часто задаваемые вопросы":
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого вопроса
        key_1 = types.InlineKeyboardButton(text='Распределение на профили', callback_data='raspredelenie')
        # И добавляем кнопку на экран
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='Узнать номер группы', callback_data='nomer')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Получить студенческий билет', callback_data='studbilet')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='Как попасть в корпус', callback_data='korpus')
        keyboard.add(key_4)
        key_5 = types.InlineKeyboardButton(text='Общежитие', callback_data='obshaga')
        keyboard.add(key_5)
        key_6 = types.InlineKeyboardButton(text='PRE-курс', callback_data='pre-kurs')
        keyboard.add(key_6)
        key_7 = types.InlineKeyboardButton(text='Личный кабинет ТИУ', callback_data='lk')
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
    elif message.text == "❓️Задать вопрос":
        bot.send_message(message.chat.id, "Пожалуйста, напишите ваш вопрос, и я постараюсь на него ответить.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет или нажми на кнопку.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
        
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    if call.data == 'medicina':
        bot.send_message(call.message.chat.id, "🏥 ЦЕНТР МЕДИЦИНСКОГО ОБЕСПЕЧЕНИЯ\n\n \nул. Володарского, 38, 3 этаж\n📞 7 (3452) 68 27 49 \nул. Нагорная, 6, 1 этаж, общежитие\n📞 7 (3452) 28 37 44 \nул. Киевская, 80, 1 этаж, общежитие \n\n⏰ Время работы: 08.00-15.00\n\n📎 https://www.tyuiu.ru/infrastruktura/centr-medicinskogo-obespeceniia/studentu")
    elif call.data == 'library':
        bot.send_message(call.message.chat.id, "Чтобы попасть в корпус...")
    elif call.data == 'dormitory':
        bot.send_message(call.message.chat.id, "Чтобы попасть в корпус...")
    elif call.data == 'institute':
        bot.send_message(call.message.chat.id, "Чтобы попасть в корпус...")
    elif call.data == 'comission':
        bot.send_message(call.message.chat.id, "Чтобы попасть в корпус...")
    elif call.data == 'corpusestyuiu':
        bot.send_message(call.message.chat.id, "Чтобы попасть в корпус...")
>>>>>>> Stashed changes


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")