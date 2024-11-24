from telebot import types
import telebot
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot('7933512901:AAFgV8RvDQH7_0UEceoMDynmunZwBBTO_MM')

# вывод на команду старт
    

@bot.message_handler(commands=['start'])
def main(message):
    # создаем клавиатуруруру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_corpuses = types.KeyboardButton("🏢Корпуса ТИУ")
    button_ask_question = types.KeyboardButton("❓️Задать вопрос")
    button_spravka = types.KeyboardButton("🔍Часто задаваемые вопросы")
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
        with open('файлы/корпус.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
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
    elif message.text == "❓Задать вопрос":
        bot.send_message(message.chat.id, "Пожалуйста, напишите ваш вопрос, и я постараюсь на него ответить.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет или нажми на кнопку.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
        
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    if  call.data == 'raspredelenie':
        bot.send_message(call.message.chat.id, "Информация для студентов ВШЦТ поступивших на 1 курс по направлению подготовки:\n\n🔄 09.03.01 Информатика и вычислительная техника (Автоматизированные системы обработки информации и управления)\n 🔄 09.03.01 Информатика и вычислительная техника (Информационная безопасность компьютерных систем и сетей)\n 🔄 09.03.02 Информационные системы и технологии (Информационные системы и технологии в геологии и нефтегазовой отрасли\n 🔄 09.03.02 Информационные системы и технологии (Искусственный интеллект и программирование)\n 🔄 09.03.02 Информационные системы и технологии (Интеллектуальные системы и технологии» Умный город»)\n 🔄 09.03.02 Информационные системы и технологии (Технология разработки и сопровождения программного продукта)\n \n Вы поступили в ВШЦТ в рамках многопрофильного конкурса, который предполагает процедуру распределения по профилям подготовки\n Вам необходимо выполнить следующее:\n 1️⃣Ознакомиться с Выпиской из инструкции \n 2️⃣Заполнить Заявление в двух вариантах заполнения ниже \n 🔄 вариант 1 распечатать заявление, подписать и принести 02.09.2024 на PRE-курс\n 🔄вариант 2 получить бланк заявления на PRE-курс, заполнить и подписать его на организационной встрече. \n \n Обращаем Ваше внимание, что в заявлении должны быть указаны все ШЕСТЬ профилей.\n Если Вы относитесь к категориям обучающихся, которые распределяются вне конкурса- необходимо принести с собой копии всех подтверждающих документов и приложить их к заявлению.")
    elif  call.data == 'nomer':
        bot.send_message(call.message.chat.id, "Узнать номер группы вы можете в файле:")
        with open('ВШЦТ_списки_1 курс_распред.pdf', 'rb') as document:
            bot.send_document(call.message.chat.id, document)
    elif call.data == 'studbilet':
        bot.send_message(call.message.chat.id, "До 30 августа необходимо принести 3 фото размером 3х4 для оформления студенческого и зачетки \n\nКуда нести? \nВ свой территориальный отдел \nул. Мельникайте д. 70, кабинет 204, 206 \n\nТакже на входе в каждый корпус будут стоять боксы, куда можно положить свои фото\n\n❗️Важно❗️\nНа Фотографиях с оборотной стороны надо написать свое ФИО полностью и название института")
    elif call.data == 'korpus':
        bot.send_message(call.message.chat.id, "Чтобы попасть в корпус...")
    elif call.data == 'obshaga':
        bot.send_message(call.message.chat.id, "...")
    elif call.data == 'pre-kurs':
        bot.send_message(call.message.chat.id, "...")
    elif call.data == 'lk':
        bot.send_message(call.message.chat.id, "Теперь расписание учебных занятий можно посмотреть в личном кабинете на платформе 'Мой ТИУ'. \nhttps://sso.tyuiu.ru \n\n❗️У вас может истечь срок действия пароля \nЕго нужно обновлять каждый год \nСоздайте новый через 'Забыл пароль' (Главное указывать почту/телефон которые вы предоставляли при поступлении)\n\nУ кого слетел пароль - инструкция 🫡⚠️\nhttps://t.me/iottyuiu22/102")
    elif call.data == 'zimbra':
        bot.send_message(call.message.chat.id,"Сброс пароля осуществляется пользователем самостоятельно, обновление происходит через сутки")
    elif call.data == 'communication':
        bot.send_message(call.message.chat.id, "...")
    elif call.data == 'poka':
        bot.send_message(call.message.chat.id, "...")
    elif call.data == 'spravka':
        bot.send_message(call.message.chat.id, "...") 
    
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
        media_group = []
        
        for i in range(1, 7):
            media_group.append(InputMediaPhoto(open(f'файлы/academic_calendar{i}.png', 'rb')))
        
        # Отправка группы медиа (фотографий)
        bot.send_media_group(chat_id=call.message.chat.id, media=media_group)

        # Отправка текстового сообщения после фотографий
        bot.send_message(call.message.chat.id, "НАПОМИНАНИЕ ☑️ \n\n"
                          "Как найти календарный учебный график (КУГ) на https://www.tyuiu.ru/ 👩‍💻 \n\n"
                          "Смотри и сохраняй инструкцию😉 \n\n"
                          "P.S. Как читать КУГ: \n\n"
                          "1️⃣ Найди строку своего курса и направления подготовки \n\n"
                          "2️⃣ Каждый столбец - шестидневная учебная неделя. Даты в заголовке таблицы стоят с учётом воскресенья, а самих клеток в столбце шесть, "
                          "потому что воскресенье - выходной по умолчанию \n\n"
                          "3️⃣ Находи в строке своего курса и направления столбец с необходимым обозначением (их расшифровка указана перед таблицей) и сверяй его с датами в шапке таблицы")
    elif call.data == 'curriculum':
        bot.send_message(call.message.chat.id, "Учебный план доступен в вашем личном кабинете...")
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

###
###