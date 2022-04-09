-- создаем таблицу mainmenu из трех полей, если она еще не была создана
-- id - главный ключ, числовой 1,2,3...
-- title - название меню
-- ссылка, на которую будем переходить, кликая по соответствующему пункту меню 
CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

-- создаем таблицу posts из двух полей, если она еще не была создана
-- id - главный ключ статьи, порядковый номер
-- title - название статьи
-- text  - текст статьи
-- time  - когда была добавлена статья в эту таблицу
-- url text - добавлено для отображения html страницы, поле по которому будет браться соответствующая статья
--            поисковые системы проще ищут статью по url, чем по id, наш url страницы будет состоять из обычного текста
--            что гораздо лучше для поисковых систем
CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
url text NOT NULL,
time integer NOT NULL
);

-- создадим таблицу users для регистрации пользователей register
-- добавим в таблицу информацию, которая помимо пользователей хранила бы и аватарку
-- BLOB - тип для хранения бинарных данных и по умолчанию принимать значение NULL
-- и далее в БД создадим таблицу users с этими полями
CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
avatar BLOB DEFAULT NULL,
time integer NOT NULL
);