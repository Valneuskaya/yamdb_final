# Проект YaMDb
![greetings!](https://github.com/Valneuskaya/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание
Проект собирает отзывы на произведения
### Технологии
Python 3.7-slim
PostgreSQL
Django 2.2.19
### Запуск проекта
pip install -r requirements.txt
### Шаблон наполнения env-файла
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
### Команды для установки зависимостей
RUN pip3 install -r /app/requirements.txt --no-cache-dir
### Команды для запуска сервера разработки при старте контейнера
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
### Автор
Валерия Невская
