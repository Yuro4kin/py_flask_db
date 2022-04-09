#  После создания экземпляра класса LoginManager добавим в наш проект еще один файл UserLogin.py
#  в котором пропишем вспомогательный класс UserLogin
#   fromDB - первый метод используется при создании объекта в декораторе user_loader
#  Он по user_id выполняет загрузку пользовательских данных из БД и сохраняет в
#  __user частном свойстве, присваиваем ему то, что возвратит метод getUser
#  getUser - берет информацию из БД по текущему пользователю с определенным id
#  return self - возвращаем экземпляр класса UserLogin
#  create - Второй метод  используется при создании объекта в момент авторизации
#  пользователя. Вся информация о нем уже известна и мы ее просто передаем по ссылке user
#  и также сохраняем в частной переменной __user. Эта информация потом пригодится в методе
#  get_id, который возвращает id текущего пользователя.

# класс UseMixin() по умолчанию реализует методы is_authenticated(), is_active(), is_anonymous() которые нам не нужны
# можем оставить только то, что сами определяем
import sqlite3
from flask import url_for
from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        return str(self.__user['id'])

    # методы аватарки которые возвращают имя и email пользователя
    # в __user хранится вся информация пользователя, которую прочитали из БД
    # класс UserLogin() создан таким способом, что в переменной __user хранится вся информация
    # if - тернарный условный оператор, name возвращаем, иначе берем без имени
    def getName(self):
        return self.__user['name'] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user['email'] if self.__user else "Без email"

    # чтоб обработчик userava() работал нужно прописать метод getAvatar() в классе UserLogin
    # if - если для нашего текущего пользователя в БД avatar отсутствует, то мы пытаемся загрузить по пути
    # app.root_path + url_for('static', filename='images/default.png' - по умолчанию
    # "rb" - загружаем файл в бинарном режиме
    # read() - читаем файл
    # retern img - возвращаем файл если нет except
    # if - если в БД уже есть аватарка if not self.__user['avatar'], то переменная img будет ссылаться на self.__user['avatar']
    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.__user['avatar']

        return img

    # метод для разделения файла с конца находим точку, остаток соответствует или png или PNG
    # если расширение png функция возвращает True
    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False


