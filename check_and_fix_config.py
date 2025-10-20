#!/usr/bin/env python3
"""
Скрипт для проверки и исправления конфигурации
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Проверить .env файл"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ Файл .env не найден!")
        return False
    
    print("📄 Проверяем .env файл...")
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Проверяем на placeholder значения
    placeholder_values = [
        'your_actual_',
        'your_bot_token',
        'your_admin_token',
        'your_marzban_url',
        'your_secret_key'
    ]
    
    issues = []
    for placeholder in placeholder_values:
        if placeholder in content:
            issues.append(placeholder)
    
    if issues:
        print(f"⚠️  Найдены placeholder значения: {', '.join(issues)}")
        return False
    else:
        print("✅ .env файл выглядит корректно")
        return True

def create_sample_env():
    """Создать пример .env файла"""
    sample_env = """# Конфигурация YoVPN бота

# Telegram Bot Token (получить у @BotFather)
USERBOT_TOKEN=your_bot_token_here

# Marzban API настройки
MARZBAN_API_URL=https://your-marzban-domain.com/api
MARZBAN_ADMIN_TOKEN=your_marzban_admin_token_here

# База данных
DATA_FILE=data.json

# Логирование
LOG_LEVEL=INFO
LOG_FILE=bot.log

# Безопасность
SECRET_KEY=your_secret_key_here
RATE_LIMIT_RPM=60
RATE_LIMIT_RPH=1000

# Мониторинг (опционально)
SENTRY_DSN=
PROMETHEUS_PORT=8000

# Redis (опционально)
REDIS_URL=redis://localhost:6379

# Платежи
DAILY_COST=4.0
MIN_BALANCE_WARNING=8.0

# Уведомления (опционально)
ADMIN_TELEGRAM_ID=
NOTIFICATION_ENABLED=true
"""
    
    with open('.env.sample', 'w') as f:
        f.write(sample_env)
    
    print("📄 Создан файл .env.sample с примером конфигурации")

def check_required_tokens():
    """Проверить обязательные токены"""
    print("\n🔍 Проверяем обязательные токены...")
    
    try:
        from src.config import config
        
        # Проверяем токен бота
        if not config.BOT_TOKEN or config.BOT_TOKEN.startswith('your_'):
            print("❌ USERBOT_TOKEN не установлен или содержит placeholder")
            print("   Получите токен у @BotFather в Telegram")
            return False
        else:
            print("✅ USERBOT_TOKEN установлен")
        
        # Проверяем Marzban API URL
        if not config.MARZBAN_API_URL or config.MARZBAN_API_URL.startswith('https://your-'):
            print("❌ MARZBAN_API_URL не установлен или содержит placeholder")
            print("   Укажите URL вашего Marzban API (например: https://your-domain.com/api)")
            return False
        else:
            print("✅ MARZBAN_API_URL установлен")
        
        # Проверяем Marzban Admin Token
        if not config.MARZBAN_ADMIN_TOKEN or config.MARZBAN_ADMIN_TOKEN.startswith('your_'):
            print("❌ MARZBAN_ADMIN_TOKEN не установлен или содержит placeholder")
            print("   Получите токен из Marzban Swagger UI")
            return False
        else:
            print("✅ MARZBAN_ADMIN_TOKEN установлен")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке конфигурации: {e}")
        return False

def test_telegram_connection():
    """Тестировать подключение к Telegram"""
    print("\n🤖 Тестируем подключение к Telegram...")
    
    try:
        from src.config import config
        import requests
        
        # Простой запрос к Telegram API
        url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✅ Подключение к Telegram успешно")
                print(f"   Бот: @{bot_info.get('username', 'unknown')}")
                print(f"   Имя: {bot_info.get('first_name', 'unknown')}")
                return True
            else:
                print(f"❌ Telegram API вернул ошибку: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP ошибка {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к Telegram: {e}")
        return False

def test_marzban_connection():
    """Тестировать подключение к Marzban"""
    print("\n🌐 Тестируем подключение к Marzban...")
    
    try:
        from src.services.marzban_service import MarzbanService
        from src.config import config
        
        marzban_service = MarzbanService(config.MARZBAN_API_URL, config.MARZBAN_ADMIN_TOKEN)
        
        # Проверяем доступность API
        if marzban_service.check_api_availability():
            print("✅ Marzban API доступен")
            return True
        else:
            print("❌ Marzban API недоступен")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к Marzban: {e}")
        return False

def main():
    """Главная функция"""
    print("🔧 Проверка конфигурации YoVPN бота")
    print("=" * 50)
    
    # Проверяем .env файл
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n📝 Создаем пример .env файла...")
        create_sample_env()
        print("\n⚠️  Пожалуйста, скопируйте .env.sample в .env и заполните реальными значениями")
        return False
    
    # Проверяем обязательные токены
    tokens_ok = check_required_tokens()
    
    if not tokens_ok:
        print("\n❌ Не все обязательные токены установлены")
        print("📝 Создаем пример .env файла...")
        create_sample_env()
        print("\n⚠️  Пожалуйста, обновите .env файл с реальными значениями")
        return False
    
    # Тестируем подключения
    telegram_ok = test_telegram_connection()
    marzban_ok = test_marzban_connection()
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ:")
    print(f"   .env файл: {'✅' if env_ok else '❌'}")
    print(f"   Токены: {'✅' if tokens_ok else '❌'}")
    print(f"   Telegram: {'✅' if telegram_ok else '❌'}")
    print(f"   Marzban: {'✅' if marzban_ok else '❌'}")
    
    if all([env_ok, tokens_ok, telegram_ok, marzban_ok]):
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОШЛИ! Бот готов к запуску.")
        return True
    else:
        print("\n⚠️  Есть проблемы с конфигурацией. Исправьте их перед запуском.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)