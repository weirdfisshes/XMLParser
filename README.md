# XMLParser
Скрипт для загрузки прайсов в БД. 
Технологии: Python, PostgreSQL, Docker, logger

Поставщик отправляет ссылку на архив с XML-файлом. Скрипт загружает файл, распаковывает архив, парсит XML-файл и сохраняет позиции из прайса в БД PostgreSQL.

Запуск осуществляется командой:

```
docker-compose up --build
```

В docker-compose необходимо добавить следующие переменные окружения:
```
PRICE_URL: # Прямая ссылка на рахив с прайсом
DATABASE_URL: # Строка соединения с PostgreSQL
```
