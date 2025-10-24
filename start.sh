#!/bin/bash

# ========================================
# YoVPN Bot - Скрипт быстрого запуска
# ========================================

set -e

echo "🚀 Запуск YoVPN Bot..."

# Проверка Python версии
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
    echo "❌ Требуется Python $required_version или выше"
    echo "📦 Текущая версия: $python_version"
    exit 1
fi

echo "✅ Python $python_version"

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
echo "🔄 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден"
    echo "📝 Создаем из .env.example..."
    cp .env.example .env
    echo "⚙️  Отредактируйте .env файл и запустите скрипт снова"
    exit 1
fi

# Проверка переменных окружения
echo "🔍 Проверка конфигурации..."
python3 -c "from config import check_config; exit(0 if check_config() else 1)"

if [ $? -ne 0 ]; then
    echo "❌ Ошибка конфигурации"
    echo "📝 Проверьте файл .env"
    exit 1
fi

# Применение миграций
echo "🗄️  Применение миграций базы данных..."
alembic upgrade head

echo ""
echo "✅ Все готово!"
echo ""
echo "🤖 Запуск бота..."
echo "📊 Логи будут выводиться ниже"
echo ""
echo "----------------------------------------"
echo ""

# Запуск бота
python bot/main.py
