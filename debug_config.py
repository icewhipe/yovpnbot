#!/usr/bin/env python3
"""
Скрипт для отладки конфигурации бота
"""

import os
import sys
import logging

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def debug_config():
    """Отладка конфигурации"""
    print("=" * 60)
    print("ОТЛАДКА КОНФИГУРАЦИИ БОТА")
    print("=" * 60)
    
    # Импортируем config
    try:
        from src.config import config
        print("✅ config.py импортирован успешно")
    except Exception as e:
        print(f"❌ Ошибка импорта config.py: {e}")
        return
    
    # Проверяем значения
    print(f"\n1. BOT_TOKEN: {config.BOT_TOKEN[:20]}..." if config.BOT_TOKEN else "BOT_TOKEN: НЕ УСТАНОВЛЕН")
    print(f"2. MARZBAN_API_URL: {config.MARZBAN_API_URL}")
    print(f"3. MARZBAN_ADMIN_TOKEN: {config.MARZBAN_ADMIN_TOKEN[:20]}..." if config.MARZBAN_ADMIN_TOKEN else "MARZBAN_ADMIN_TOKEN: НЕ УСТАНОВЛЕН")
    
    # Проверяем, как decouple читает переменные
    print("\n" + "=" * 40)
    print("ПРОВЕРКА DECOUPLE")
    print("=" * 40)
    
    try:
        from decouple import config as decouple_config
        
        # Проверяем каждую переменную отдельно
        bot_token = decouple_config('USERBOT_TOKEN', default='test_token')
        api_url = decouple_config('MARZBAN_API_URL', default='https://test.com/api')
        admin_token = decouple_config('MARZBAN_ADMIN_TOKEN', default='test_token')
        
        print(f"1. USERBOT_TOKEN: {bot_token[:20]}..." if bot_token != 'test_token' else "USERBOT_TOKEN: test_token")
        print(f"2. MARZBAN_API_URL: {api_url}")
        print(f"3. MARZBAN_ADMIN_TOKEN: {admin_token[:20]}..." if admin_token != 'test_token' else "MARZBAN_ADMIN_TOKEN: test_token")
        
        # Проверяем файл .env
        print(f"\n4. Файл .env существует: {os.path.exists('.env')}")
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                content = f.read()
                print(f"5. Содержимое .env:")
                for line in content.strip().split('\n'):
                    if line.strip():
                        print(f"   {line}")
        
        # Проверяем переменные окружения
        print(f"\n6. Переменные окружения:")
        print(f"   USERBOT_TOKEN: {os.getenv('USERBOT_TOKEN', 'НЕ УСТАНОВЛЕНА')}")
        print(f"   MARZBAN_API_URL: {os.getenv('MARZBAN_API_URL', 'НЕ УСТАНОВЛЕНА')}")
        print(f"   MARZBAN_ADMIN_TOKEN: {os.getenv('MARZBAN_ADMIN_TOKEN', 'НЕ УСТАНОВЛЕНА')}")
        
    except Exception as e:
        print(f"❌ Ошибка с decouple: {e}")
    
    # Проверяем, есть ли другие .env файлы
    print("\n" + "=" * 40)
    print("ПОИСК .ENV ФАЙЛОВ")
    print("=" * 40)
    
    import glob
    env_files = glob.glob("**/.env*", recursive=True)
    print(f"Найдено .env файлов: {len(env_files)}")
    for env_file in env_files:
        print(f"  - {env_file}")
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                print(f"    Содержимое:")
                for line in content.strip().split('\n'):
                    if line.strip():
                        key, value = line.split('=', 1)
                        if 'TOKEN' in key or 'PASSWORD' in key:
                            print(f"      {key}={value[:20]}..." if len(value) > 20 else f"      {key}={value}")
                        else:
                            print(f"      {key}={value}")
        except Exception as e:
            print(f"    Ошибка чтения: {e}")
        print()

if __name__ == "__main__":
    debug_config()