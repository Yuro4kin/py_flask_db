# Flask #7: Регистрация пользователей и шифрование паролей
#
import sqlite3
import os
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash



DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

app = Flask(__name__)


app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

# декоратор перехвата запросов
# before_request() - функция работает перед выполнением запроса
# FDataBase() - создание экземпляра класса
# чтоб переменная dbase была доступна во всех запросах мы сделали ее глобальной
# global dbase - говорит, что внутри функции будем обращаться к переменной dbase, так мы вынесли за скобку общий код
# теперь можно в функциях представления использовать переменную dbase вместо строк
dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()



@app.route("/")
def index():
    # db = get_db()              - теперь используем глобальную переменную dbase
    # dbase = FDataBase(db)
    return render_template('index.html', menu = dbase.getMenu(), posts=dbase.getPostsAnonce())



@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    # db = get_db()
    # dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('ERROR  of add post', category='error')
            else:
                flash('Post added successfully', category='success')
        else:
            flash('ERROR  of add post', category='error')

    return render_template('addpost.html', menu=dbase.getMenu(), title="Add post")


@app.route("/post/<alias>")
def showPost(alias):
#    db = get_db()
#    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)

# обработчик для url - login, возвращаем шаблон login.html
@app.route("/login")
def login():
    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")

# обработчик для формы регистрации
# @app.route("/register")
# def register():
#     return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")

# обработчик для формы регистрации c шифрованием паролей в БД
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.pop('_flashes', None)
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")


# Шифрование паролей в БД, переходим в Python Console
# >>> from werkzeug.security import generate_password_hash, check_password_hash
# >>> hash = generate_password_hash("12345")
# >>> hash
# 'pbkdf2:sha256:260000$S19ICVOKSAI75HVh$67aae21a318f37c3281bd041339f547b8d1f05de9945d8df16a99bdbc6606c4a'
# Для проверки корректности ввода пароля используется функция check_password_hash(hash, "12345"), если они равны True
# >>> heck_password_hash(hash, "12345")
# True



# webserver start
if __name__ == "__main__":
    app.run(debug=True)




# Test
# http://127.0.0.1:5000/           : GET / HTTP/1.1" 200
# http://127.0.0.1:5000/register   : GET /register HTTP/1.1" 200

# art@ukrt.net  parol:12347
# Error - если регистрируем и e-mail совпадает