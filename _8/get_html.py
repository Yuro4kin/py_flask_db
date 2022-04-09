import webbrowser
import requests

# Библиотека - документация
# http://requests.readthedocs.org
# Requests: HTTP for Humans™ — Requests 2.27.1 ...


webbrowser.open('https://proproprogs.ru/flask/flask-chto-eto-takoe-wsgi-prilozhenie')


# Записать веб-страницу в файл можно в цикле for, используя метод iter_
# content () объекта Response.
#                      Получаем HTML code страницы

res = requests.get('https://proproprogs.ru/flask/flask-chto-eto-takoe-wsgi-prilozhenie')
# Error:              https://inventwithpython.com/page_that_does_not_exist

# https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


print(type(res))
print(res.status_code == requests.codes.ok)
print(len(res.text))
print(res.text[:250])

# Обработка Error
try:
    res.raise_for_status()
except Exception as exc:
    print('Возникла проблема: %s' % (exc))

# Записать веб-страницу в файл можно в цикле for, используя метод iter_
# content () объекта Response.
playFile = open('index.html', 'wb')
for chunk in res.iter_content(100000): # Размер фрагмента в байтах 100000 = 100 Килобайт 
    playFile.write(chunk)

playFile.close()

