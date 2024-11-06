# vyatsuparser
Vyatsu Schedule Parser

Парсер расписания вашей группы в формат JSON.

## 1. Настройте подключение к базе данных
Замените строчку  mongo в файле  config.py на подключение к вашей Базе Данных
Создайте Базу Данных UsersData и в ней коллекцию vyatsu


## 2 Импортируйте модуль rasp_parse.py в ваш проект


## Пример использования

```
import rasp_parse

parse=rasp_parse.rasp_parse()
if parse=={}:
      rasp_parse.login()
      parse=rasp_parse.rasp_parse()


```
