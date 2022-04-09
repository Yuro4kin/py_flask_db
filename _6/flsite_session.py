# Flask #6: Порядок работы с сессиями (session)

from flask import Flask, render_template, make_response, request, url_for, session
import  datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '53faaab6e4d79c4c1b753d881feb1325c40fd54a'
app.permanent_session_lifetime = datetime.timedelta(days=10)

# сессии работают по похожему с cookies принципу: они также хранятся в браузере в виде особых кук
# сессий, но дополнительно шифруются с помощью ключа, который можно задать в WSGI-приложении
# SECRET_KEY - помогает работать с session, шифровальный ключ
# Для надежности этот ключ должен содержать самые разные символы
# и один из хороших способов его сгенерировать в Python Console – это воспользоваться следующей командой пакета os:
# >>> import os
# >>> os.urandom(20).hex()
#     '53faaab6e4d79c4c1b753d881feb1325c40fd54a'
# импортируем объект session, который доступен как в программах так и в шаблонах

# функция представления index() с помощью session будет подсчитывать колличество посещений главной страницы
# if - проверяем существует ли такое свойство visits в объекте session, и если оно не существует мы создаем это свойство со значением 1
#      если условие срабатывает 'visits' in session - значение которое там есть увеличиваем на 1
# return - на странице отображаем колличество просмотров из этой сессии
# передача session данных переходит браузеру только в том случае, если состояние объекта session меняется


# session_data() при первом запросе формируем поле data, которое ссылается на список data.
# if - если свойство 'data' в этой сессии отсутствует , то мы его создаем и передаем ссылку на список
# if - если data существует, берем второй элемент списка data и каждый раз будем увеличивать на 1
# return - отображаем.
# Т.е. обновляя страницу /session мы каждый раз должны видеть увеличение второго элемента каждый раз на 1
# А при последующих запросах происходит увеличение второго элемента этого списка на 1.
# По идее, при обновлении страницы, мы должны видеть постоянное увеличение второго значения на 1.
# Давайте посмотрим, обновляем, но ничего не происходит. Почему? Как раз по той причине,
# что объект session в этом случае никак не меняется: он как ссылался на список,
# так и ссылается (адрес списка остается прежним). Меняется лишь элемент в самом списке
# и это изменение не влияет на изменение session. А раз так, то Flask решает, что сессия
# не поменялась и нет смысла нагружать канал связи и дополнительно ее отправлять браузеру.
# session.modified = True - Flask поймет, что объект сессии изменился, и его нужно снова передать браузеру
#                           так можно указать что session обновилась в браузере клиента
# чтоб session не пропали как лиент закроет браузер пропишем и тогда время хранения session устанавливаетс
# с помощью app.permanent_session_lifetime, по умолчанию параметр 31 день
# если хотим, чтоб session.permanent = False не сохранялась



# обработчик главной страницы декоратора route
@app.route("/")
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # обновление данных сессии
    else:
        session['visits'] = 1  # запись данных в сессию

    return f"<h1>Main Page</h1>Число просмотров: {session['visits']}"

# создадим функцию представления
data = [1, 2, 3, 4]
@app.route("/session")
def session_data():
    session.permanent = True
    #                   False
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True

    return f"session['data']: {session['data']}"


# webserver start
if __name__ == "__main__":
    app.run(debug=True)

# Test
#  http://127.0.0.1:5000/           :    GET / HTTP/1.1" 200
#  http://127.0.0.1:5000/session    :    GET /session HTTP/1.1" 200