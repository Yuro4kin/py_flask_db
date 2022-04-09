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
CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
time integer NOT NULL
);