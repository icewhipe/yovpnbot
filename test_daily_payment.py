#!/usr/bin/env python3
"""
Скрипт для тестирования системы ежедневной оплаты
"""

import os
import sys
import logging
import time
from datetime import datetime, timedelta

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import config
from src.services.user_service import UserService
from src.services.marzban_service import MarzbanService
from src.services.daily_payment_service import DailyPaymentService
from src.services.notification_service import NotificationService

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_daily_payment_system():
    """Тестирование системы ежедневной оплаты"""
    logger.info("=== ТЕСТ СИСТЕМЫ ЕЖЕДНЕВНОЙ ОПЛАТЫ ===")
    
    # Создание сервисов
    user_service = UserService()
    marzban_service = MarzbanService()
    notification_service = NotificationService()
    daily_payment_service = DailyPaymentService(marzban_service, user_service)
    
    # Проверяем доступность Marzban API
    if not marzban_service.health_check():
        logger.error("Marzban API недоступен!")
        return False
    
    logger.info("✅ Marzban API доступен")
    
    # Тестовые данные
    test_user_id = 123456789
    test_username = "testuser"
    
    # Создаем тестового пользователя
    logger.info(f"Создаем тестового пользователя: {test_username}")
    user = user_service.ensure_user_record(test_user_id, test_username, "Test User")
    
    # Начисляем баланс (20 рублей = 5 дней)
    user_service.add_balance(test_user_id, 20)
    logger.info(f"Начислен баланс: 20 ₽")
    
    # Проверяем баланс
    balance = user_service.get_balance(test_user_id)
    days = user_service.days_from_balance(test_user_id)
    logger.info(f"Баланс: {balance} ₽, дней: {days}")
    
    # Создаем пользователя в Marzban
    logger.info("Создаем пользователя в Marzban...")
    created_user = marzban_service.create_user(test_username, test_user_id, days=1)
    if created_user:
        logger.info("✅ Пользователь создан в Marzban")
    else:
        logger.error("❌ Не удалось создать пользователя в Marzban")
        return False
    
    # Тестируем ежедневную обработку
    logger.info("Тестируем ежедневную обработку...")
    
    # Симулируем списание за 1 день
    logger.info("Симулируем списание за 1 день...")
    result = daily_payment_service._process_user_payment(
        test_user_id, 
        test_username, 
        {"username": test_username}
    )
    
    if result == 'processed':
        logger.info("✅ Списание прошло успешно")
        
        # Проверяем новый баланс
        new_balance = user_service.get_balance(test_user_id)
        new_days = user_service.days_from_balance(test_user_id)
        logger.info(f"Новый баланс: {new_balance} ₽, дней: {new_days}")
        
        # Проверяем подписку в Marzban
        user_info = marzban_service.get_user_info(test_username)
        if user_info:
            logger.info(f"Статус подписки: {user_info.get('status')}")
            logger.info(f"Дней до истечения: {user_info.get('days_remaining')}")
        
    else:
        logger.error(f"❌ Ошибка списания: {result}")
        return False
    
    # Тестируем уведомления
    logger.info("Тестируем уведомления...")
    
    # Симулируем низкий баланс
    user_service.update_user_balance(test_user_id, 2)  # 2 рубля = меньше 1 дня
    logger.info("Установлен низкий баланс: 2 ₽")
    
    # Проверяем необходимость уведомления
    should_notify = daily_payment_service._should_send_low_balance_notification(test_user_id, 2)
    if should_notify:
        logger.info("✅ Уведомление о низком балансе необходимо")
        daily_payment_service._send_low_balance_notification(test_user_id, 2)
        logger.info("✅ Уведомление отправлено")
    else:
        logger.info("ℹ️ Уведомление не требуется")
    
    # Тестируем приостановку подписки
    logger.info("Тестируем приостановку подписки...")
    result = daily_payment_service._process_user_payment(
        test_user_id, 
        test_username, 
        {"username": test_username}
    )
    
    if result == 'suspended':
        logger.info("✅ Подписка приостановлена")
        
        # Проверяем статус в Marzban
        user_info = marzban_service.get_user_info(test_username)
        if user_info:
            logger.info(f"Статус подписки после приостановки: {user_info.get('status')}")
    else:
        logger.error(f"❌ Ошибка приостановки подписки: {result}")
        return False
    
    logger.info("=== ТЕСТ ЗАВЕРШЕН УСПЕШНО ===")
    return True

def test_notification_service():
    """Тестирование сервиса уведомлений"""
    logger.info("=== ТЕСТ СЕРВИСА УВЕДОМЛЕНИЙ ===")
    
    notification_service = NotificationService()
    
    # Тестируем различные типы уведомлений
    test_user_id = 123456789
    
    # Уведомление о списании
    logger.info("Тестируем уведомление о списании...")
    notification_service.send_payment_notification(test_user_id, 4, 16, 'charged')
    
    # Уведомление о приостановке
    logger.info("Тестируем уведомление о приостановке...")
    notification_service.send_payment_notification(test_user_id, 0, 2, 'suspended')
    
    # Уведомление о низком балансе
    logger.info("Тестируем уведомление о низком балансе...")
    notification_service.send_low_balance_notification(test_user_id, 2)
    
    # Уведомление о приветственном бонусе
    logger.info("Тестируем уведомление о приветственном бонусе...")
    notification_service.send_welcome_bonus_notification(test_user_id, 20, 20)
    
    logger.info("=== ТЕСТ УВЕДОМЛЕНИЙ ЗАВЕРШЕН ===")

if __name__ == "__main__":
    try:
        # Тестируем систему ежедневной оплаты
        if test_daily_payment_system():
            logger.info("✅ Все тесты прошли успешно!")
        else:
            logger.error("❌ Тесты не прошли!")
        
        # Тестируем сервис уведомлений
        test_notification_service()
        
    except Exception as e:
        logger.error(f"Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()