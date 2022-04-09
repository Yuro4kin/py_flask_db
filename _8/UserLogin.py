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

class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])

