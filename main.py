import pymysql
import pymysql.cursors
import telebot
from telebot import types
from config import host, user, password, db_name
#подключение к БД
nv = []
tv = []
chat = 0
idfp = 0
adm = [132969936, 960361521]
try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected...")
    print(" " * 20)
    # запуск кода

    bot = telebot.TeleBot("5372505442:AAEkCpHCkK59SpotKYpUVFdzQ2W2xh8fNOM")

    @bot.message_handler(commands=['start'], func=lambda message: message.chat.id in adm)

    def start(message):
        bot.send_message(message.chat.id, '<b>Доброго времени суток, '+''+'. Чего желаете?</b>', parse_mode='html')

    def adddef(message):
        global nv
        adddef = message.text
        if (adddef == 'Нет' or adddef == 'нет' or adddef == 'НЕТ'):
            nv.append('NULL')
        else:
            nv.append(adddef)
        print(nv)
        new = nv[0]
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO votes (question, ans1, ans2, ans3, ans4, ans5, ans6, ans7, ans8, ans9, ans10, rightans, descr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nv[0], nv[1], nv[2], nv[3], nv[4], nv[5], nv[6], nv[7], nv[8], nv[9], nv[10], nv[11], nv[12]))
            connection.commit()

            id = cursor.execute("select max(id) from votes")
            ids = cursor.fetchall()
            connection.commit()
            x=ids[0]['max(id)']
        bot.send_message(message.chat.id, 'Отлично, ваш опрос успешно создан. Номер опроса для публикации: <b>'+str(x)+'</b>', parse_mode='html')
        nv = []

    def group1(message):
        global chat
        chat = -1001738481240
        publ(message)

    def groupnew(message):
        nmes = bot.send_message(message.chat.id, "Хорошо, введите номер id группы...", parse_mode='html')
        bot.register_next_step_handler(nmes, addnewgroup)

    def addnewgroup(message):
        global chat
        chat = int(message.text)
        publ(message)

    def grouptest(message):
        global chat
        chat = -773955573
        publ(message)

    def here(message):
        global chat
        chat = message.chat.id
        publ(message)

    def group(message):
        if message.text != "Отмена" and message.text != "отмена":
            global idfp
            idfp = message.text
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            item_group1 = types.InlineKeyboardButton("Physics. ITMO. 2022. Mechanics", callback_data='group1')
            item_test= types.InlineKeyboardButton("Test Group", callback_data='grouptest')
            item_here = types.InlineKeyboardButton("Опубликовать тут", callback_data='here')
            item_newgroup = types.InlineKeyboardButton("Новая группа", callback_data='groupnew')

            markup_inline.add(item_group1, item_test, item_here, item_newgroup)

            bot.send_message(message.chat.id, 'Выберите место публикации...', reply_markup=markup_inline)
        else:
            bot.send_message(message.chat.id, "Вы отменили действие", parse_mode='html')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        if call.message:
            if call.data == "group1":
                group1(call.message)
            elif call.data == "grouptest":
                grouptest(call.message)
            elif call.data == "here":
                here(call.message)
            elif call.data == "groupnew":
                groupnew(call.message)


    def publ(message):
        global idfp
        global chat
        if len(message.text) <=4:
            idfp = int(message.text)
        with connection.cursor() as cursor:
            id = cursor.execute("SELECT `question`, `ans1`, `ans2`, `ans3`, `ans4`, `ans5`, `ans6`, `ans7`, `ans8`, `ans9`, `ans10`, `rightans`, `descr` FROM `votes` WHERE id = %s",(idfp))
            ids = cursor.fetchall()
            if ids != ():
                connection.commit()
                quest = ids[0]['question']
                rightans = int(ids[0]['rightans'][-1])-1
                descr = ids[0]['descr']
                dd = [ids[0]['ans1'], ids[0]['ans2'], ids[0]['ans3'], ids[0]['ans4'], ids[0]['ans5'], ids[0]['ans6'], ids[0]['ans7'], ids[0]['ans8'], ids[0]['ans9'], ids[0]['ans10']]
                anslist = []
                for aa in dd:
                    if aa != 'NULL': anslist.append(aa)

                bot.send_poll(chat, quest, anslist, False, 'quiz', None, rightans, descr )
            else:
                nmes = bot.send_message(message.chat.id, "Такого номера не существует, введите корректный",
                                        parse_mode='html')
                bot.register_next_step_handler(nmes, publ)

    def addright(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2] == 's'):
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,
                                    "Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            mes6 = bot.send_message(message.chat.id,
                                    "Введите правильный ответ, формат указан выше",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, addright)


    def ans10done(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2] == 's'):
            nv.append('NULL')
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,
                                    "Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            nv.append(ans4)
            bot.send_message(message.chat.id, "Вы добавили максимальное количество вариантов ", parse_mode='html')
            mes6 = bot.send_message(message.chat.id,
                                    "Введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, addright)

    def ans9done(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2] == 's'):
            nv.append('NULL')
            nv.append('NULL')
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,
                                    "Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            nv.append(ans4)
            bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
            mes6 = bot.send_message(message.chat.id,
                                    "Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, ans10done)

    def ans8done(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2] == 's'):
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,
                                    "Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            nv.append(ans4)
            bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
            mes6 = bot.send_message(message.chat.id,
                                    "Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, ans9done)

    def ans7done(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2] == 's'):
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,
                                    "Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            nv.append(ans4)
            bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
            mes6 = bot.send_message(message.chat.id,
                                    "Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, ans8done)

    def ans6done(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2] == 's'):
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,
                                    "Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            nv.append(ans4)
            bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
            mes6 = bot.send_message(message.chat.id,
                                    "Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, ans7done)

    def ans5done(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2] == 's'):
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,
                                    "Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            nv.append(ans4)
            bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
            mes6 = bot.send_message(message.chat.id,
                                    "Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",
                                    parse_mode='html')
            bot.register_next_step_handler(mes6, ans6done)

    def ans4done(message):
        global nv
        ans4 = message.text
        if (ans4[0] == 'a' and ans4[1] == 'n' and ans4[2]=='s'):
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append('NULL')
            nv.append(ans4)
            mes6 = bot.send_message(message.chat.id,"Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",parse_mode='html')
            bot.register_next_step_handler(mes6, adddef)
        else:
            nv.append(ans4)
            bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
            mes6 = bot.send_message(message.chat.id, "Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:", parse_mode='html')
            bot.register_next_step_handler(mes6, ans5done)

    def ans3done(message):
        global nv
        if message.text != "Отмена" and message.text != "отмена":
            ans3 = message.text
            if (ans3[0] == 'a' and ans3[1] == 'n' and ans3[2]=='s'):
                nv.append('NULL')
                nv.append('NULL')
                nv.append('NULL')
                nv.append('NULL')
                nv.append('NULL')
                nv.append('NULL')
                nv.append('NULL')
                nv.append('NULL')
                nv.append(ans3)
                mes5 = bot.send_message(message.chat.id,"Правильный ответ успешно добавлен. Хотите ли вы добавить какое-то описание к опросу?",parse_mode='html')
                bot.register_next_step_handler(mes5, adddef)
            else:
                nv.append(ans3)
                bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
                mes5 = bot.send_message(message.chat.id, "Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:", parse_mode='html')
                bot.register_next_step_handler(mes5, ans4done)
        else:
            bot.send_message(message.chat.id, "Вы отменили действие", parse_mode='html')
            nv = []

    def ans2done(message):
        global nv
        if message.text != "Отмена" and message.text != "отмена":
            ans2 = message.text
            nv.append(ans2)
            bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
            mes4 = bot.send_message(message.chat.id,"Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",parse_mode='html')
            bot.register_next_step_handler(mes4, ans3done)
        else:
            bot.send_message(message.chat.id, "Вы отменили действие", parse_mode='html')
            nv = []

    def ans1done(message):
        global nv
        if message.text != "Отмена" and message.text != "отмена":
            ans1 = message.text
            nv.append(ans1)
            mes3 = bot.send_message(message.chat.id, "Для создания опроса необходимо добавить ещё хотя бы 1 вариант:", parse_mode='html')
            bot.register_next_step_handler(mes3, ans2done)
        else:
            bot.send_message(message.chat.id, "Вы отменили действие", parse_mode='html')
            nv = []

    def questdone(message):
        global nv
        if message.text != "Отмена" and message.text != "отмена":
            quest = message.text
            nv.append(quest)
            mes2 = bot.send_message(message.chat.id, "Теперь введите первый вариант ответа на ваш вопрос:", parse_mode='html')
            bot.register_next_step_handler(mes2, ans1done)
        else:
            bot.send_message(message.chat.id, "Вы отменили действие", parse_mode='html')
            nv = []


    def newvote(message):
        mes = bot.send_message(message.chat.id, "Для создания опроса введите вопрос", parse_mode='html')
        bot.register_next_step_handler(mes, questdone)




    @bot.message_handler(func=lambda message: message.chat.id in adm)
    def getusermessage(message):
        if message.text == "Опрос" or message.text == 'опрос'or message.text == 'ОПРОС':
            newvote(message)
        elif message.text == "Опубликовать" or message.text == "опубликовать":
            #nmes = bot.send_message(message.chat.id, "Хотите опубликовать опрос сейчас?", parse_mode='html')
            nmes = bot.send_message(message.chat.id, "Хорошо, введите номер опроса...", parse_mode='html')
            bot.register_next_step_handler(nmes, group)
            #bot.register_next_step_handler(nmes, prepubl)




    bot.polling(none_stop=True)
except Exception as ex:
    print("Connection refused...")
    print(ex)
