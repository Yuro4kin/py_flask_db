import sqlite3
import math
import time

# класс FDataBase: записан ниже
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
    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)", (title, text, tm))
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
    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return (False, False)

#   метод getPostsAnonce() для выбора SELECT всех записей из нашей таблицы posts, которая отсортирована от самой свежей и менее свежей статьи
#   fetchall() - с помощью метода получаем все записи в виде словаря
#   if - если записи были получены успешно, то мы их возвращаем. Иначе формируется ошибка. Если ошибка произошла, то мы возвращаем пустой список
#   выполнена реализация получения всех статей из БД, который будут отображаться в шаблоне index.html
    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return []