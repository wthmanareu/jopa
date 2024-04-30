from flask import Flask
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from data import db_session
from data.users import User
from data.saveOfField import SavedField
from data.shipBattleScript import *
from data.drawer import *
from data.savesDecoder import *
from data.imageFinderYandexMaps import *
from data.test import *
from data.geographicTestResult import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/dataOfUsers.db")
geographicQuestions = [["Россия", 0], ["Америка", 0], ["Гренландия", 0], ["Африка", 0], ["Великобритания", 0],
                       ["Франция", 0], ["Германия", 0], ["Испания", 0], ["Польша", 0], ["Украина", 0],
                       ["КИТАЙ", 0], ["Бразилия", 0], ["Италия", 0], ["Япония", 0], ["Индонезия", 0],
                       ["Красная площадь", 1, "https://img4.goodfon.ru/wallpaper/nbig/a/f2/kremlin-moskva-rossiia-kreml-moscow-krasnaia-ploshchad.jpg"],
                       ["Стоунхендж", 1, "https://24tv.ua/resources/photos/news/201512/641076.jpg?1537444773000"],
                       ["Эйфелева башня", 1, "https://cdn.pixabay.com/photo/2018/11/25/15/24/eiffel-tower-3837629_1280.jpg"],
                       ["Великая китайская стена", 1, 'https://international.wallscafe.com/wp-content/uploads/2019/10/The-Great-Wall-of-China-with-Green-Vegetation.jpg'],
                       ["Пирамида хеопса", 1, 'https://1.bp.blogspot.com/-1WUFXqgZk28/VXVf1l6rzpI/AAAAAAAAHig/f6EAHYX-BSk/s1600/367A0069.JPG']]


def start(update, context):
    update.message.reply_text("Привет я бот который может играть в морской бой\n"
                              "но для начала вам нужно зарегистрироваться /register или войти /login")
    context.user_data["userID"] = None
    context.user_data["nameForChek"] = None
    context.user_data["name"] = None
    return 8


def choose(update, context):
    update.message.reply_text("зарегистрироваться /register войти /login")
    return 8


def registerName(update, context):
    update.message.reply_text("Придумайте имя:")
    name = update.message.text
    context.user_data["nameForChek"] = name
    return 5


def registerName2(update, context):
    name = update.message.text
    context.user_data["nameForChek"] = name
    update.message.reply_text("Придумайте пароль:")
    return 6


def registerPass(update, context):
    name = context.user_data["nameForChek"]
    password = update.message.text
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.name == name).first() == None:
        user = User()
        user.name = name
        user.password = password
        db_sess.add(user)
        db_sess.commit()
        userInfo = db_sess.query(User).filter(User.name == name).first()
        context.user_data["name"] = name
        context.user_data["userID"] = userInfo.id
        update.message.reply_text(f"Вы вошли под именем {context.user_data['name']}")
        update.message.reply_text(
            "можете сыграть в морской бой используя команду /ship или пройти географический тест /geo")
        update.message.reply_text("Можете снова зарегистрироваться или войти /menuNewStart")
        return 9
    else:
        update.message.reply_text("Пользователь с таким именем существует\n"
                                  "зарегистрироваться /register войти /login")
        return 8


def loginName(update, context):
    update.message.reply_text("Введите имя:")
    name = update.message.text
    context.user_data["nameForChek"] = name
    return 2


def loginName2(update, context):
    name = update.message.text
    context.user_data["nameForChek"] = name
    update.message.reply_text("Введите пароль:")
    return 3


def loginPass(update, context):
    password = update.message.text
    name = context.user_data["nameForChek"]
    db_sess = db_session.create_session()
    userInfo = db_sess.query(User).filter(User.name == name).first()
    if userInfo != None:
        if userInfo.password == password:
            context.user_data["name"] = name
            context.user_data["userID"] = userInfo.id
            update.message.reply_text(f"Вы вошли под именем {context.user_data['name']}")
            update.message.reply_text("можете сыграть в морской бой используя команду /ship или пройти географический тест /geo")
            update.message.reply_text("Можете снова зарегистрироваться или войти /menuNewStart")
            db_sess.commit()
            return 9
    update.message.reply_text("неправильный пароль или логин\n"
                                      "зарегистрироваться /register войти /login")
    return 8


def startPlayChoiceText(update, context):
    update.message.reply_text("можете сыграть в морской бой используя команду /ship или пройти географический тест /geo")
    update.message.reply_text("Можете снова зарегистрироваться или войти /menuNewStart")
    return 9


def shipBattleSaveOrNewGame(update, context):
    update.message.reply_text(
        "вы можете продолжить последние сохранение командой /loadLastSave или начать новую игру /startNewGame")
    update.message.reply_text("Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
    return 10


def startNewGame(update, context):
    context.user_data["FieldStartGame"] = GameField()
    context.user_data["ship4"] = 0
    context.user_data["ship3"] = 0
    context.user_data["ship2"] = 0
    context.user_data["ship1"] = 0
    GF = context.user_data["FieldStartGame"]
    update.message.reply_photo(photo=open(board(GF.botMapForUser, context.user_data["name"]), 'rb'),
                               caption=f"Сейчас вам надо раставить корабли\n"
                                       "программа сама выберет размер корябля по очереди от 4 до 1 вам только "
                                       "надо вводить данные в таком формате:\n "
                                       "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                       "столбце(буква)> или за вас расставять всё автоматически /auto")
    update.message.reply_text("Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
    return 11


def autoField(update, context):
    context.user_data["FieldStartGame"] = GameField()
    GF = context.user_data["FieldStartGame"]
    GF.autoCreate()
    update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'), caption="ваше поле")
    update.message.reply_photo(photo=open(board(GF.botMapForUser, context.user_data["name"]), 'rb'), caption="поле противника")
    try:
        os.remove(f'static/img/imagesForShipGame/{context.user_data["name"]}.png')
    except BaseException:
        pass
    if GF.whoIsTurn == 0:
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        update.message.reply_text("Сейчас ваш ход надо вводить данные в таком формате:\n "
                                  "<позиция в строке(число)> <позиция в столбце(буква)>")
        return 12
    else:
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        update.message.reply_text("сейчас ход робота введите любой текст чтобы он сходил или можете сохранить игру командой /save")
        return 13


def shipPlace(update, context):
    GF = context.user_data["FieldStartGame"]
    if context.user_data["ship4"] == 0:
        txt = update.message.text
        txt = txt.split()
        if len(txt) != 3:
            update.message.reply_text(
                "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
            update.message.reply_text("надо вводить данные в таком формате:\n "
                                     "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                     "столбце(буква)>")
        else:
            if not GF.placeShip(GF.userMap, 4, txt[0], int(txt[1]), txt[2]):
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                update.message.reply_text("надо вводить данные в таком формате:\n "
                                          "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                          "столбце(буква)>")
            else:
                update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'))
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                context.user_data["ship4"] += 1
        return 11
    elif context.user_data["ship3"] < 2:
        txt = update.message.text
        txt = txt.split()
        if len(txt) != 3:
            update.message.reply_text(
                "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
            update.message.reply_text("надо вводить данные в таком формате:\n "
                                     "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                     "столбце(буква)>")
        else:
            if not GF.placeShip(GF.userMap, 3, txt[0], int(txt[1]), txt[2]):
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                update.message.reply_text("надо вводить данные в таком формате:\n "
                                          "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                          "столбце(буква)>")
            else:
                update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'))
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                context.user_data["ship3"] += 1
        return 11
    elif context.user_data["ship2"] < 3:
        txt = update.message.text
        txt = txt.split()
        if len(txt) != 3:
            update.message.reply_text(
                "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
            update.message.reply_text("надо вводить данные в таком формате:\n "
                                     "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                     "столбце(буква)>")
        else:
            if not GF.placeShip(GF.userMap, 2, txt[0], int(txt[1]), txt[2]):
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                update.message.reply_text("надо вводить данные в таком формате:\n "
                                          "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                          "столбце(буква)>")
            else:
                update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'))
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                context.user_data["ship2"] += 1
        return 11
    elif context.user_data["ship1"] < 4:
        txt = update.message.text
        txt = txt.split()
        if len(txt) != 3:
            update.message.reply_text(
                "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
            update.message.reply_text("надо вводить данные в таком формате:\n "
                                     "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                     "столбце(буква)>")
        else:
            if not GF.placeShip(GF.userMap, 1, txt[0], int(txt[1]), txt[2]):
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                update.message.reply_text("надо вводить данные в таком формате:\n "
                                          "<поворот(влево, вправо, вниз, вверх)> <позиция в строке(число)> <позиция в "
                                          "столбце(буква)>")
            else:
                update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'))
                update.message.reply_text(
                    "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
                context.user_data["ship1"] += 1
        return 11
    elif GF.whoIsTurn == 0:
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        update.message.reply_text("Сейчас ваш ход надо вводить данные в таком формате:\n "
                                          "<позиция в строке(число)> <позиция в столбце(буква)>")
        return 12
    else:
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        update.message.reply_text("сейчас ход робота введите любой текст чтобы он сходил или можете сохранить игру командой /save")
        return 13


def gamePlayStartPlayer(update, context):
    GF = context.user_data["FieldStartGame"]
    txt = update.message.text
    txt = txt.split()
    result = GF.shotUser(int(txt[0]), txt[1])
    if result == 1:
        update.message.reply_text("вы попали")
    else:
        update.message.reply_text("вы промахнулись")
    update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'), caption="ваше поле")
    update.message.reply_photo(photo=open(board(GF.botMapForUser, context.user_data["name"]), 'rb'), caption="поле противника")
    try:
        os.remove(f'static/img/imagesForShipGame/{context.user_data["name"]}.png')
    except BaseException:
        pass
    if GF.shipCountBot > 0:
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        if GF.whoIsTurn == 0:
            update.message.reply_text("Сейчас ваш ход надо вводить данные в таком формате:\n "
                                      "<позиция в строке(число)> <позиция в столбце(буква)>\n"
                                      "можете сохранить игру командой /save")
            return 12
        else:
            update.message.reply_text(
                "сейчас ход робота введите любой текст чтобы он сходил или можете сохранить игру командой /save")
            return 13
    else:
        try:
            os.remove(f'static/img/imagesForShipGame/{context.user_data["name"]}.png')
        except BaseException:
            pass
        update.message.reply_text(
            "вы победили")
        update.message.reply_text(
            "можете сыграть в морской бой используя команду /ship или пройти географический тест /geo")
        context.user_data["FieldStartGame"].restart()
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart")
        return 9


def gamePlayStartBot(update, context):
    GF = context.user_data["FieldStartGame"]
    GF.bot.hod()
    update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'), caption="ваше поле")
    update.message.reply_photo(photo=open(board(GF.botMapForUser, context.user_data["name"]), 'rb'), caption="поле противника")
    try:
        os.remove(f'static/img/imagesForShipGame/{context.user_data["name"]}.png')
    except BaseException:
        pass
    if GF.shipCountUser > 0:
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        if GF.whoIsTurn == 1:
            update.message.reply_text(
                "сейчас ход робота введите любой текст чтобы он сходил или можете сохранить игру командой /save")
            return 13
        else:
            update.message.reply_text("Сейчас ваш ход надо вводить данные в таком формате:\n "
                                      "<позиция в строке(число)> <позиция в столбце(буква)>\n"
                                      "можете сохранить игру командой /save")
            return 12
    else:
        try:
            os.remove(f'static/img/imagesForShipGame/{context.user_data["name"]}.png')
        except BaseException:
            pass
        update.message.reply_text(
            "бот победил")
        update.message.reply_text(
            "можете сыграть в морской бой используя команду /ship или пройти географический тест /geo")
        context.user_data["FieldStartGame"].restart()
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart")
        return 9


def save(update, context):
    GF = context.user_data["FieldStartGame"]
    db_sess = db_session.create_session()
    if db_sess.query(SavedField).filter(SavedField.userId == context.user_data["userID"]).first() == None:
        fieldSave = SavedField()
        fieldSave.userId = context.user_data["userID"]
        fieldSave.userField = decode(GF.userMap)
        fieldSave.enemyFieldUser = decode(GF.botMapForUser)
        fieldSave.userShipCount = GF.shipCountUser
        fieldSave.enemyField = decode(GF.botMap)
        fieldSave.enemyShipCount = GF.shipCountBot
        fieldSave.enemyHodi = decode(GF.bot.hodi)
        fieldSave.enemyLst = ','.join(list(map(str, GF.bot.lst)))
        fieldSave.enemyDrctx = ','.join(list(map(str, GF.bot.drctx)))
        fieldSave.enemyDrctx2 = ','.join(list(map(str, GF.bot.drctx2)))
        fieldSave.drctForShot = decode(GF.bot.drctForShot)
        fieldSave.whoIsTurn = GF.whoIsTurn
        db_sess.add(fieldSave)
        db_sess.commit()
    else:
        fieldSave = db_sess.query(SavedField).filter(SavedField.userId == context.user_data["userID"]).first()
        fieldSave.userId = context.user_data["userID"]
        fieldSave.userField = decode(GF.userMap)
        fieldSave.enemyFieldUser = decode(GF.botMapForUser)
        fieldSave.userShipCount = GF.shipCountUser
        fieldSave.enemyField = decode(GF.botMap)
        fieldSave.enemyShipCount = GF.shipCountBot
        fieldSave.enemyHodi = decode(GF.bot.hodi)
        fieldSave.enemyLst = ','.join(list(map(str, GF.bot.lst)))
        fieldSave.enemyDrctx = ','.join(list(map(str, GF.bot.drctx)))
        fieldSave.enemyDrctx2 = ','.join(list(map(str, GF.bot.drctx2)))
        fieldSave.drctForShot = decode(GF.bot.drctForShot)
        fieldSave.whoIsTurn = GF.whoIsTurn
        db_sess.commit()


def loadLastSave(update, context):
    db_sess = db_session.create_session()
    if db_sess.query(SavedField).filter(SavedField.userId == context.user_data["userID"]).first() != None:
        fieldSave = db_sess.query(SavedField).filter(SavedField.userId == context.user_data["userID"]).first()
        context.user_data["FieldStartGame"] = GameField(encode(fieldSave.enemyField), encode(fieldSave.userField),
                                                        encode(fieldSave.enemyFieldUser), fieldSave.userShipCount,
                                                        fieldSave.enemyShipCount, encode(fieldSave.enemyHodi),
                                                        encode(fieldSave.drctForShot), list(map(int, fieldSave.enemyLst.split(','))),
                                                        list(map(int, fieldSave.enemyDrctx.split(','))),
                                                        list(map(int, fieldSave.enemyDrctx2.split(','))), fieldSave.whoIsTurn)
        GF = context.user_data["FieldStartGame"]
        update.message.reply_photo(photo=open(board(GF.userMap, context.user_data["name"]), 'rb'), caption="ваше поле")
        update.message.reply_photo(photo=open(board(GF.botMapForUser, context.user_data["name"]), 'rb'),
                                   caption="поле противника")
        try:
            os.remove(f'static/img/imagesForShipGame/{context.user_data["name"]}.png')
        except BaseException:
            pass
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        if GF.whoIsTurn == 0:
            update.message.reply_text("Сейчас ваш ход надо вводить данные в таком формате:\n "
                                      "<позиция в строке(число)> <позиция в столбце(буква)>")
            return 12
        else:
            update.message.reply_text(
                "сейчас ход робота введите любой текст чтобы он сходил или можете сохранить игру командой /save")
            return 13
    else:
        update.message.reply_text(
            "у вас нет сохранений можете начать новую игру командой /startNewGame")
        return 50


def normal(string):
    return string.lower().replace(".", "").replace(",", "").replace("-", "").replace("?", "").replace("!", "").replace(
        ":", "")


def geographicTestStart(update, context):
    sp = []
    for i in range(10):
        obj = choice(geographicQuestions)
        while obj in sp:
            obj = choice(geographicQuestions)
        sp.append(obj)
    context.user_data["GeoTest"] = sp
    context.user_data["RightAnwsersGeoTest"] = 0
    txt = context.user_data["GeoTest"].pop()
    context.user_data["Answer"] = normal(txt[0])
    if txt[1] == 1:
        update.message.reply_photo(photo=open(saveImgYandex(txt[2], context.user_data["name"]), 'rb'), caption="Что это")
    else:
        update.message.reply_photo(
            photo=open(save_geo(txt[0], 'sat', f'static/img/imagesForGeographicTest/{context.user_data["name"]}.png', '20', True),
                       'rb'), caption="Что это за страна")
    update.message.reply_text(
        "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
    try:
        os.remove(f'static/img/imagesForGeographicTest/{context.user_data["name"]}.png')
    except BaseException:
        pass
    return 15


def geographicTestPlay(update, context):
    answer = normal(update.message.text)
    if answer == context.user_data["Answer"]:
        context.user_data["RightAnwsersGeoTest"] += 1
        update.message.reply_text("Правильно")
    else:
        update.message.reply_text("Неправильно")
    if len(context.user_data["GeoTest"]) > 0:
        txt = context.user_data["GeoTest"].pop()
        context.user_data["Answer"] = normal(txt[0])
        if txt[1] == 1:
            update.message.reply_photo(photo=open(saveImgYandex(txt[2], context.user_data["name"]), 'rb'), caption="Что это")
        else:
            update.message.reply_photo(
                photo=open(
                    save_geo(txt[0], 'sat', f'static/img/imagesForGeographicTest/{context.user_data["name"]}.png',
                             '20', True),
                    'rb'), caption="Что это за страна")
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart или вернуться к выбоу игры /chooseGame")
        try:
            os.remove(f'static/img/imagesForGeographicTest/{context.user_data["name"]}.png')
        except BaseException:
            pass
        return 15
    else:
        try:
            os.remove(f'static/img/imagesForGeographicTest/{context.user_data["name"]}.png')
        except BaseException:
            pass
        update.message.reply_text(
            f"У вас {context.user_data['RightAnwsersGeoTest']} правильных ответов и {10 - context.user_data['RightAnwsersGeoTest']}"
            f" неправильных")
        db_sess = db_session.create_session()
        saveOfGeoTest = db_sess.query(GeographicTest).filter(GeographicTest.userId == context.user_data["userID"]).first()
        if saveOfGeoTest != None:
            update.message.reply_text(
                f"В прошлый раз у вас было {saveOfGeoTest.userResult} правильных ответов и {10 - saveOfGeoTest.userResult}"
                f" неправильных")
            saveOfGeoTest.userId = context.user_data["userID"]
            saveOfGeoTest.userResult = context.user_data['RightAnwsersGeoTest']
        else:
            saveOfGeoTest = GeographicTest()
            saveOfGeoTest.userId = context.user_data["userID"]
            saveOfGeoTest.userResult = context.user_data['RightAnwsersGeoTest']
            db_sess.add(saveOfGeoTest)
        db_sess.commit()
        update.message.reply_text(
            "можете сыграть в морской бой используя команду /ship или пройти географический тест /geo")
        update.message.reply_text(
            "Можете снова зарегистрироваться или войти /menuNewStart")
        return 9


def stop(update, context):
    update.message.reply_text("досвидания")
    context.user_data["name"] = None
    return ConversationHandler.END


def botStart(key):
    updater = Updater(key, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, loginName, pass_user_data=True)],
            2: [MessageHandler(Filters.text, loginName2, pass_user_data=True)],
            3: [MessageHandler(Filters.text, loginPass, pass_user_data=True)],
            4: [MessageHandler(Filters.text, registerName, pass_user_data=True)],
            5: [MessageHandler(Filters.text, registerName2, pass_user_data=True)],
            6: [MessageHandler(Filters.text, registerPass, pass_user_data=True)],
            7: [MessageHandler(Filters.text, startPlayChoiceText, pass_user_data=True)],
            8: [CommandHandler("login", loginName), CommandHandler("register", registerName)],
            9: [CommandHandler("ship", shipBattleSaveOrNewGame), CommandHandler("geo", geographicTestStart),
                CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText)],
            10: [CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText),
                 CommandHandler("startNewGame", startNewGame), CommandHandler('loadLastSave', loadLastSave)],
            11: [CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText),
                 CommandHandler("auto", autoField), MessageHandler(Filters.text, shipPlace, pass_user_data=True)],
            12: [CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText),
                 CommandHandler('save', save), MessageHandler(Filters.text, gamePlayStartPlayer)],
            13: [CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText),
                 CommandHandler('save', save), MessageHandler(Filters.text, gamePlayStartBot)],
            14: [CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText),
                 MessageHandler(Filters.text, geographicTestStart)],
            15: [CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText),
                 MessageHandler(Filters.text, geographicTestPlay)],
            50: [CommandHandler("menuNewStart", start), CommandHandler("chooseGame", startPlayChoiceText),
                 CommandHandler("startNewGame", startNewGame)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()