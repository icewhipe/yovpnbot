# YoVPN Bot Dockerfile
# Современный многоэтапный Dockerfile для продакшена

# Этап 1: Базовый образ
FROM python:3.11-slim as base

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для безопасности
RUN groupadd -r yovpn && useradd -r -g yovpn yovpn

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements-prod.txt .

# Устанавливаем Python зависимости (только production)
RUN pip install --no-cache-dir -r requirements-prod.txt

# Этап 2: Сборка приложения
FROM base as builder

# Копируем исходный код
COPY . .

# Создаем директории для данных
RUN mkdir -p data uploads temp logs

# Устанавливаем права доступа
RUN chown -R yovpn:yovpn /app

# Этап 3: Финальный образ
FROM base as production

# Копируем приложение из builder
COPY --from=builder /app /app

# Переключаемся на пользователя yovpn
USER yovpn

# Открываем порты
EXPOSE 8000 8080

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Создаем health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Запускаем приложение
CMD ["python", "bot/main.py"]