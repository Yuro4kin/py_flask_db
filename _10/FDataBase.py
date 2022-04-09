import sqlite3
import math
import time
import re
from flask import url_for

# addUser() - добавляет пользователя в БД


# db - ссылка на связь с БД, которую сохраняем в экземпляре этого класса self.__db
# __cur - сразу создаем экземпляр класс cursor(), через этот экземпляр класса __cur работаем с таблицами БД
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    #  в методе getMenu() который мы вызываем потом производим выборку всех записей из таблицы mainmenu
    #  try -  в этом блоке мы пытаемся прочитать данные из этой таблицы
    #  except - может таблицы mainmenu нет в БД, также это исключение нужно, чтоб негативно не повлияло на работу нашего сайта
    #           при отработке except функция getMenu() возвратит пустой список
    # execute()  - это метод класса __cur которому передаем запрос sql
    # fetchall() - это метод класса __cur с помощью которого вычитываем все записи
    # if         - возвращаем записи res, если были прочитаны успешно
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Error reading from database")
        return []

#   addPost() -  пропишем метод, который добавляет данные в таблицу posts, принимает два параметра title, text
#   try - взять текущее время добавления статьи, math - чтоб округлить время
#   INSERT INTO posts - sql запрос, и берем данные из кортежа (title, text, tm)
#   commit() - созхраняет физически в БД запись
#   - проверка уникальности url
#   url - третий аргумент и параметр для обработки поля url из формы, еще один ? и параметр url
#          нужно проверить, существует ли такая запись с url
#   SELECT COUNT() - выберем url, где он должен совпадать с url который передали
#   count > 0 - выполняем False, значит статья уже существует с таким url и функция addPost() вернет False, и дальше функция addPost() не пойдет
    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("An article with this url already exists")
                return False

            # re - модуль для пути изображений
            base = url_for('static', filename='images_html')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>>",
                          text)

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding post to database" + str(e))
            return False

        return True


#   добавим getPost() - метод который будет брать данные из БД в файл
#   принимает параметр postId по которому мы вибираем SLECT статью posts из БД
#   выбираем SELECT заголовок title текст text, id должно совпадать с id которое мы передали
#   fetchone() - используем метод, возьмем одну запись
#   if - если res неравно NONE, т.е. запись успешно получена, то мы ее возвращаем в виде кортежа
#   иначе формирую ошибку Error и возвращаю значение false
#   переходим на сайт и отображаем статью = 1, http://127.0.0.1:5000/post/1
#   изменим в методе второй аргумент с postId на alias для отображения url на странице
#   url LIKE alias - url будет совпадать с строкой alias
#   re - корректировка адресов изображений после проверки if res:, где переменная base будет ссылаться на каталог static
    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return (res)
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return (False, False)

#   метод getPostsAnonce() для выбора SELECT всех записей из нашей таблицы posts, которая отсортирована от самой свежей и менее свежей статьи
#   fetchall() - с помощью метода получаем все записи в виде словаря
#   if - если записи были получены успешно, то мы их возвращаем. Иначе формируется ошибка. Если ошибка произошла, то мы возвращаем пустой список
#   выполнена реализация получения всех статей из БД, который будут отображаться в шаблоне index.html
#   - метод getPostsAnonce() возвращает также список статей, добавим url, чтоб возвращал запись соответствующей статьи, перейдем в index.html, добавим alias
    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return []

    # класс FDataBase: вспогательный класс для обработки БД ,записан ниже
    # NULL - хранение аватарки, когда регистрируется новый пользователь должна создаваться аватарка по умолчанию, для этого изменим addUser() в FDataBase()
    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        return True

    # определим метод getUser в классе FDataBase
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False


    # эим методом мы передаем в качестве параметров email
    # SELECT - выбираем все поля из таблицы users по email
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

        # метод изменения аватарки пользователя, если параметр avatar не содержит данных, то
        # возвращаем false и работа функции updateUserAvatar() завершается
        # try - иначе помещаем аватарку в БД, для этого мы должны .Binary() бинарные данные преобразовать в объект
        # UPDATE - поместить бинарный объект в БД, поле аватар меняем на поле binary
        # commit() - сохраняем изменение в БД

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True