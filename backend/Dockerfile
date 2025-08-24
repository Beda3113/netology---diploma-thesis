# Dockerfile
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВЕСЬ проект (включая manage.py и папки)
COPY . .

# Собираем статику 
RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Запускаем Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "procurement_backend.wsgi"]
