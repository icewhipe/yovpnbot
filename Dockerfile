FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем директорию для данных
RUN mkdir -p /app/data

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app
USER botuser

# Переменные окружения
ENV PYTHONPATH=/app
ENV DATA_FILE=/app/data/bot_data.json

# Команда запуска
CMD ["python", "main_improved.py"]