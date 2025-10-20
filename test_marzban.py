#!/usr/bin/env python3
"""
Тестовый скрипт для проверки подключения к Marzban API
"""

import os
import sys
import logging

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import config
from src.services.marzban_service import MarzbanService

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_marzban_connection():
    """Тестируем подключение к Marzban API"""
    print("=" * 50)
    print("ТЕСТ ПОДКЛЮЧЕНИЯ К MARZBAN API")
    print("=" * 50)
    
    # Показываем текущую конфигурацию
    print(f"API URL: {config.MARZBAN_API_URL}")
    print(f"Admin Token: {config.MARZBAN_ADMIN_TOKEN[:10]}..." if config.MARZBAN_ADMIN_TOKEN else "НЕ УСТАНОВЛЕН")
    print()
    
    # Создаем сервис
    marzban_service = MarzbanService()
    
    # Тестируем подключение
    print("Проверяем доступность API...")
    is_healthy = marzban_service.health_check()
    
    if is_healthy:
        print("✅ Marzban API доступен!")
        
        # Пробуем получить системную информацию
        print("\nПолучаем системную информацию...")
        system_info = marzban_service._make_request('GET', '/system')
        if system_info:
            print("✅ Системная информация получена:")
            print(f"   Версия: {system_info.get('version', 'Неизвестно')}")
            print(f"   Статус: {system_info.get('status', 'Неизвестно')}")
        else:
            print("❌ Не удалось получить системную информацию")
    else:
        print("❌ Marzban API недоступен!")
        print("\nВозможные причины:")
        print("1. Неправильный URL API")
        print("2. Неправильный токен администратора")
        print("3. Marzban сервер не запущен")
        print("4. Проблемы с сетью")
        print("5. SSL сертификат недействителен")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_marzban_connection()