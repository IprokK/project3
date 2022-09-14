import pymysql
import pymysql.cursors
import telebot
from config import host, user, password, db_name
#подключение к БД
nv = []
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

    @bot.message_handler(commands=['start'])

    def start(message):
        print(message)
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

        # connection.commit()

    def publ(message):
        id = (message.text)
        with connection.cursor() as cursor:
            id = cursor.execute("SELECT `question`, `ans1`, `ans2`, `ans3`, `ans4`, `ans5`, `ans6`, `ans7`, `ans8`, `ans9`, `ans10`, `rightans`, `descr` FROM `votes` WHERE id = %s",(id))
            ids = cursor.fetchall()
            if ids != ():
                connection.commit()
                quest = ids[0]['question']
                rightans = ids[0]['rightans'][-1]
                descr = ids[0]['descr']
                dd = [ids[0]['ans1'], ids[0]['ans2'], ids[0]['ans3'], ids[0]['ans4'], ids[0]['ans5'], ids[0]['ans6'], ids[0]['ans7'], ids[0]['ans8'], ids[0]['ans9'], ids[0]['ans10']]
                anslist = []
                for aa in dd:
                    if aa != 'NULL': anslist.append(aa)

                bot.send_poll(message.chat.id, quest, anslist, False, 'quiz', None, rightans, descr )
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

    def ans2done(message):
        global nv
        ans2 = message.text
        nv.append(ans2)
        bot.send_message(message.chat.id, "Вы можете добавить ещё один вариант ответ ", parse_mode='html')
        mes4 = bot.send_message(message.chat.id,"Если считаете, что уже достаточно, то введите 'ans1' без ковычек, где вместо 1 - номер правильного ответа:",parse_mode='html')
        bot.register_next_step_handler(mes4, ans3done)

    def ans1done(message):
        global nv
        ans1 = message.text
        nv.append(ans1)
        mes3 = bot.send_message(message.chat.id, "Для создания опроса необходимо добавить ещё хотя бы 1 вариант:", parse_mode='html')
        bot.register_next_step_handler(mes3, ans2done)

    def questdone(message):
        global nv
        quest = message.text
        nv.append(quest)
        mes2 = bot.send_message(message.chat.id, "Теперь введите первый вариант ответа на ваш вопрос:", parse_mode='html')
        bot.register_next_step_handler(mes2, ans1done)


    def newvote(message):
        nv = []
        mes = bot.send_message(message.chat.id, "Для создания опроса введите вопрос", parse_mode='html')
        bot.register_next_step_handler(mes, questdone)


    @bot.message_handler()
    def getusermessage(message):
        if message.text == "Опрос" or message.text == 'опрос'or message.text == 'ОПРОС':
            newvote(message)

            #with connection.cursor() as cursor:
                #a = "INSERT INTO votes (question, ans1, ans2, rightans) VALUES (quest, ans1, 'Нет', 'ans1')"
                #c = cursor.execute(a)
                #print(c)

                #connection.commit()
        if message.text == "Опубликовать" or message.text == "опубликовать":
            nmes = bot.send_message(message.chat.id, "Для публикации опроса введите его номер...", parse_mode='html')
            bot.register_next_step_handler(nmes, publ)

    bot.polling(none_stop=True)
except Exception as ex:
    print("Connection refused...")
    print(ex)
