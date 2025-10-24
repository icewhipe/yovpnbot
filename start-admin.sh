#!/bin/bash

# ========================================
# YoVPN Admin Panel - Скрипт запуска
# ========================================

set -e

echo "🎛️ Запуск YoVPN Admin Panel..."

# Активация виртуального окружения
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Виртуальное окружение не найдено"
    echo "💡 Сначала запустите: ./start.sh"
    exit 1
fi

# Проверка .env
if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден"
    echo "📝 Скопируйте .env.example в .env и настройте"
    exit 1
fi

# Загрузка переменных окружения
export $(cat .env | grep -v '^#' | xargs)

# Порт по умолчанию
ADMIN_PORT=${ADMIN_PORT:-8080}

echo "✅ Все готово!"
echo ""
echo "🌐 Admin Panel будет доступен по адресу:"
echo "   http://localhost:$ADMIN_PORT/admin"
echo ""
echo "📊 Логи будут выводиться ниже"
echo ""
echo "----------------------------------------"
echo ""

# Запуск админ-панели
uvicorn admin.main:app --host 0.0.0.0 --port $ADMIN_PORT --reload
