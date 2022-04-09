# Flask #1: Создание БД, установление и разрыв соединения при запросах
#           В БД сохраняется вся изменяемая информация, которая потом используется при формировании ответов на запросы пользователей
import sqlite3
import os
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g


# 1. например мы можем сохранить в БД меню сайта и при формировании html страницы брать оттуда информацию и предоставлять в виде меню на странице
#    используем БД SQLite - import sqlite3

# выполним конфигурацию текущего WSGI DB приложения. Правило Flask - все переменные заглавными буквами относятся к конфигурационной информации
# DATABASE   - путь к нашему файлу
# DEBUG      - устанавливает режим отладки нашего приложения, True значит включено
# SECRET_KEY -
DATABASE = '/tmp/flask_1_create_DB_connect_sql.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

app = Flask(__name__)

# 1. Загружаем нашу конфигурацию DATABASE, DEBUG, SECRET_KEY из нашего приложения с помощью метода
#    from_object(), __name__ - это мы указываем из какого модуля мы будем загружать нашу конфигурацию
#    __name__ - это директива, которая указывает на этот текущий модуль, на основе переменных формируем начальную конфигурацию
#    теперь приложение создано, переопределим путь к БД
#    root_path - ссылается на текущий каталог данного приложения, этому приложению добавим файл 'flsite.db'
#    теперь сформирован полный путь к нашей БД
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask_1_create_DB_connect_sql.db')))
# 1. Концепция создания БД --> создание таблиц без запуска web server --> затем обработчики запросов обращаются к созданным табблицам БД
#    и затем записывают и считывают из них информацию
#    Создадим общую функцию для установления соединения с БД - вызываем sqlite3 и методу connect передаем путь где расположена наша БД
#    т.е. берем ее из конфигурации нашего приложения. row_factory - чтоб записи из БД были в виде словаря, а не в виде кортежей, словарь удобно использовать в шаблонах
#    функция возвращает установленное соединение conn
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn
# 1. объявим функцию, которая создаст БД, без запуска web server, просто создаем БД с набором таблиц
#    connect_db() - вызываем функцию, которую выше объявили
#    with...      - вызываем менеджер контекста, чтоб прочитать файл из рабочего каталога приложения
#    sq_db.sql    - файл в котором написан набор скриптов для создания таблиц сайта, mode='r' - открыт файл на чтение
#    db.cursor()  - берем соединение из БД, через класс cursor выполняем метод executescript
#    executescript() - метод запускает выполнение тех скриптов SQL, которые были прочитаны из файла
#    f.read()     - читаем скрипты и соответственно выполняем
#    db.commit()  -  после того как все сделано, записываем изменения в БД
#    db.close()   - сохраняем таблицу и закрываем соединение с БД
def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

# server - Python console
# create_db() - незапуская  сервер можем вызвать ф-цию create_db() - на реальном сервере так не работают
# переходим для работы в python console, где мы можем выполнять любые команды python
# на сервере можно делать тоже самое
# >>> from flask_1_create_DB_connect_sql import create_db
#     из нашего файла импортируем ф-цию create_db


# get_db() - функция соединения с БД
# когда приходит запрос, то создается контекст приложения, в этом контексте есть глобальная переменная g,
# в которую мы можем записать любую пользовательскую информацию. Запишем в g - установление соединения с БД
# if - проверяем существует ли у этого объекта g свойство db, если существует это св-во, значит соединение с БД было уже установлено
# если есть, то возвращаем функцией, return g.link_db
# если впервые устанавливаем соединение вызываем функцию connect_db(), которая прописана выше устанавливает соединение с нашей БД
def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# использование БД после обработки запросов
# пришел запрос       --> установилось соединение с БД (можно отследить в обработчике)
# завершение запроса  --> разрыв соединения с БД
# обработчик главной страницы добавим на наш сайта
# route - декоратор с главной страницей и функцией index
# get_db() - функция соединения с БД
# render_template() - обработчик возвращает index.html
@app.route("/indexdb")
def index():
    db = get_db()
    return render_template('indexdb.html', menu = [])


# разорвать соединение с БД
# используем декоратор teardown_appcontext - срабатывает, когда происходит уничтожение контекста приложения, обычно происходит в момент окончания обработки запроса
# декоратор является обработчиком для завершения работы с БД
# error - если будут какие-то ошибки, то в параметре будут отображаться
# if - проверяем, если в контексте нашего глобального приложения g существует св-во link_db, значит соединение с БД было установлено
# .close() - закроем соединение с БД обратився к соединению g.link_db
@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

# webserver start
if __name__ == "__main__":
    app.run(debug=True)




# Test
# http://127.0.0.1:5000/indexdb - 200 - "GET /indexdb HTTP/1.1" 