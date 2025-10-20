#!/usr/bin/env python3
"""
Симуляция запуска бота для отладки
"""

import os
import sys
import logging

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def simulate_bot_start():
    """Симуляция запуска бота"""
    print("=" * 60)
    print("СИМУЛЯЦИЯ ЗАПУСКА БОТА")
    print("=" * 60)
    
    try:
        # Импортируем config
        from src.config import config
        print("✅ config.py импортирован")
        
        # Импортируем MarzbanService
        from src.services.marzban_service import MarzbanService
        print("✅ MarzbanService импортирован")
        
        # Создаем сервис
        marzban_service = MarzbanService()
        print("✅ MarzbanService создан")
        
        # Проверяем значения
        print(f"\n1. API URL: {marzban_service.api_url}")
        print(f"2. Admin Token: {marzban_service.admin_token[:20]}..." if marzban_service.admin_token else "Admin Token: НЕ УСТАНОВЛЕН")
        
        # Тестируем подключение
        print("\n3. Тестируем подключение...")
        is_healthy = marzban_service.health_check()
        print(f"   Результат: {'✅ Здоров' if is_healthy else '❌ Недоступен'}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simulate_bot_start()