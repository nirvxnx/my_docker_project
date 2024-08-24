# Используем базовый образ Python
FROM python:3.9-slim
# Устанавливаем зависимости
RUN pip install psycopg2-binary flask

# Копируем приложение в контейнер
COPY app.py /app.py
# Запускаем Flask-приложение
CMD ["python", "app.py"]

