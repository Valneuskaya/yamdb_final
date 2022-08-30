FROM python:3.7-slim

# Сделать директорию /app рабочей директорией.
WORKDIR /app

# Скопировать содержимое директории /api_yamdb c локального компьютера
# в директорию /app.
COPY .. /app

# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r /app/requirements.txt --no-cache-dir

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
