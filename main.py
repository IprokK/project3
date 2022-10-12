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
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)
print("successfully connected...")
print(" " * 20)

bot = telebot.TeleBot("5734720458:AAFtu2kCNLjet6k_JXm9hX0f6GIJ2ErR7D0")

@bot.message_handler(commands=['start'])

def start(message):
    if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
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

#001уточнение
"""
Ниже находятся 4 функций, каждая из которых отвечает за вариант, куда можно отправить опрос. Сам id - значение chat
group1 - чат группы Z3101 
addnewgroup - чат, который не добавлен изначально(новый чат). Будет работать при условии, что Бот находится в чате и может
публиковать туда сообщения. при этом groupnew не несёт в себе чата, а лишь ссылается на функцию добавления нового чата.
grouptest - тестовый чат, в котором можно проверять правильный ли опрос вы выбрали, уточнять, правильно ли работает бот.
here - функция, которая просто отправит опрос в чат с ботом
"""

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
            new_quiz = bot.send_poll(chat, quest, anslist, False, 'quiz', None, rightans, descr )
            cursor.execute("INSERT INTO pvotes (vid, rightans) VALUES (%s, %s)",(new_quiz.poll.id, rightans))
            connection.commit()
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

def addrating(mes):
    surname = mes.text.split()[1]
    name = mes.text.split()[2]
    if name[-1] == ",":
        name = name[:-1]


    with connection.cursor() as cursor:
        cursor.execute("SELECT rating FROM rating WHERE surname = %s and name = %s",(surname, name))
        rates = cursor.fetchall()
        if rates != ():
            cursor.execute(
                "UPDATE rating SET rating = rating + 1 WHERE surname = %s and name = %s", (surname, name))
            connection.commit()
        else:
            cursor.execute(
                "INSERT INTO rating (surname, name, rating) VALUES (%s, %s, 1)", (surname, name))
            connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("SELECT rating FROM rating WHERE surname = %s and name = %s",(surname, name))
        rates = cursor.fetchall()
        check = rates[0]['rating']
    bot.send_message(mes.chat.id, ("Вы добавили пользователю "+ surname +" "+ name +" 1 балл. Итого общий балл: " +str(check)))
    print("Админ добавил пользователю "+ surname +" "+ name +" 1 балл. Итого общий балл: " +str(check))

def delrating(mes):
    surname = mes.text.split()[1]
    name = mes.text.split()[2]
    if name[-1] == ",":
        name = name[:-1]

    with connection.cursor() as cursor:
        cursor.execute("SELECT rating FROM rating WHERE surname = %s and name = %s", (surname, name))
        rates = cursor.fetchall()
        if rates != ():
            cursor.execute(
                "UPDATE rating SET rating = rating - 1 WHERE surname = %s and name = %s", (surname, name))
            connection.commit()
            check = rates[0]['rating']-1
            bot.send_message(mes.chat.id, ("Вы сняли пользователю " + surname + " " + name + " 1 балл. Итого общий балл: " + str(check)))
            print("Админ снял пользователю " + surname + " " + name + " 1 балл. Итого общий балл: " + str(check))
        else:
            bot.send_message(mes.chat.id, "Ошибка! У пользователя и так нет баллов.")

def rating(mes):
    with connection.cursor() as cursor:
        mov = []
        cursor.execute("SELECT * FROM rating ")
        rates = cursor.fetchall()
        for i in rates:
            mov.append(str(i["surname"]) +" "+ str(i["name"]) +" "+ str(i["rating"]))
        bot.send_message(mes.chat.id, '\n'.join(mov))

def setnew(mes):
    surname = mes.text.split()[1]
    name = mes.text.split()[2]
    ball = mes.text.split()[3]

    with connection.cursor() as cursor:
        cursor.execute("SELECT rating FROM rating WHERE surname = %s and name = %s", (surname, name))
        rates = cursor.fetchall()
        if rates != ():
            cursor.execute(
                "UPDATE rating SET rating = %s WHERE surname = %s and name = %s", (ball, surname, name))
            connection.commit()
        else:
            cursor.execute(
                "INSERT INTO rating (surname, name, rating) VALUES (%s, %s, %s)", (surname, name, ball))
            connection.commit()

    bot.send_message(mes.chat.id,
                     ("Вы установили пользователю " + surname + " " + name +" " +ball + " балл"))
    print("Админ установил пользователю " + surname + " " + name +" " +ball + " балл")

def vresults(mes):
    with connection.cursor() as cursor:
        mov = []
        cursor.execute("SELECT * FROM quizrate ")
        rates = cursor.fetchall()
        for i in rates:
            mov.append(str(i["surname"]) +" "+ str(i["name"]) +" "+ str(i["rate"]))
        bot.send_message(mes.chat.id, '\n'.join(mov))

#Основные команды

#002уточнение:
"""
Писать боту могут только те пользователи, которые прошли условие:
if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
Оно проверяет не id чата, а именно id человека, который отправил сообщение, таким образом,
Условие работает и в общих чатах. Это условие прописано к каждой команде, так что для того, 
чтобы дать доступ к определённой команде для всех, достаточно просто убрать эту страку и убрать 1 табуляцию 
у строки после этой.
для того, чтобы добавить ещё пользователей в белый присок нужно перед ":" добавить or message.from_user.id == id, где
вместо "id" id пользователя, которого хотите добавить
"""

@bot.message_handler()
def getusermessage(message):
    if message.text == "Опрос" or message.text == 'опрос'or message.text == 'ОПРОС':
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            newvote(message)
    elif message.text == "Опубликовать" or message.text == "опубликовать":
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            nmes = bot.send_message(message.chat.id, "Хорошо, введите номер опроса...", parse_mode='html')
            bot.register_next_step_handler(nmes, group)
    elif message.text == "+":
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            addrating(message.reply_to_message)
    elif message.text == "-":
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            bot.send_message(message.chat.id, "Ошибка не была засчитана!")
    elif message.text == "--":
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            delrating(message.reply_to_message)
    elif message.text == "рейтинг" or message.text == "Рейтинг" or message.text == "РЕЙТИНГ":
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            rating(message)
    elif message.text.split()[0] == "Установить" or message.text.split()[0] == "установить" or message.text.split()[0] == "Set":
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            setnew(message)
    elif message.text == "результаты" or message.text == "Результаты" or message.text == "РЕЗУЛЬТАТЫ":
        if message.from_user.id == 132969936 or message.from_user.id == 5663898672:
            vresults(message)


@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    surname = pollAnswer.user.last_name
    name = pollAnswer.user.first_name
    with connection.cursor() as cursor:
        cursor.execute("SELECT `rightans` FROM pvotes WHERE vid = %s",(int(pollAnswer.poll_id)))
        right = cursor.fetchall()
    if  pollAnswer.option_ids[0] == right[0]["rightans"]:
        with connection.cursor() as cursor:
            cursor.execute("SELECT rate FROM quizrate WHERE surname = %s and name = %s", (surname, name))
            rates = cursor.fetchall()
            if rates != ():
                cursor.execute(
                    "UPDATE quizrate SET rate = rate + 1 WHERE  surname = %s and name = %s", (surname, name))
                connection.commit()
            else:
                cursor.execute(
                    "INSERT INTO quizrate (surname, name, rate) VALUES (%s, %s, 1)", (surname, name))
                connection.commit()


if __name__ == "__main__":
    bot.polling(none_stop=True)

# Печатную инструкцию к боту оставлю тут:
#     -------------------------------------------------------------------------------------------------------------------
#     Первая команда - /start - функционала особого не имеет, но служит запуском диалога с ботом - для чатов использовать
#     не нужно.
#     Следующая команда - "Опрос" - создаёт опрос, после ввода команды есть инструкция, что именно нужно написать
#     !!! В поле ans*, где вместо * цифра НЕОБХОДИМО указывать цифру, соответствующую тому ответу, который был добавлен.
#     В противном случае бот при публикации не сможет опубликовать опрос и будет выдавать ошибку в консоль
#     Третья команда - "Опубликовать" - публикует опрос в один из чатов.
#     По чатам конкретнее - #001уточнение
#     Для двух последних команд действует функция "Отмена".
#     Система рейтинга:
#     "+" - одобрить исполнение - добавить балл
#     "-" - не одобрять исправления. Бот сам на пишет, что исправление не защитано
#     "--" - снять балл с пользователя
#     все эти команды работают только с ответом на сообщение типа: слово Фамилия Имя слова, при этом после имени может ничего не быть,
#     1 и 2 элемент строки, имеется ввиду через пробел, должны быть обязательно.
#     Команда "Рейтинг" (обновил до возможности писать и с большой буквы) не требует Reply. Выводит всех учеников из таблицы.
#     Проверка на то, что человек может обращаться к боту описана в #002уточнение
#     Новая команда "Установить"/"Set". Пример использования: Set Фамилия Имя балл
