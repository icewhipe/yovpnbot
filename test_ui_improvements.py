#!/usr/bin/env python3
"""
Скрипт для тестирования улучшений UI/UX
"""

import os
import sys
import logging
from datetime import datetime

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.animation_service import StickerService
from src.services.ui_service import UIService
from src.services.copy_service import CopyService
from src.services.interaction_service import InteractionService

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_ui_services():
    """Тестирование UI сервисов"""
    logger.info("=== ТЕСТ UI СЕРВИСОВ ===")
    
    # Создание сервисов
    ui_service = UIService()
    copy_service = CopyService()
    interaction_service = InteractionService()
    sticker_service = StickerService()
    
    # Тестируем создание кнопок
    logger.info("Тестируем создание кнопок...")
    
    # Тест главного меню
    user_stats = {
        'balance': 20,
        'days_remaining': 5,
        'referrals_count': 2,
        'referral_income': 24
    }
    
    keyboard = ui_service.create_main_menu_keyboard(user_stats, has_subscription=True)
    logger.info(f"✅ Главное меню создано: {len(keyboard.keyboard)} рядов кнопок")
    
    # Тест клавиатуры подписки
    subscription_info = {
        'status': 'active',
        'days_remaining': 5,
        'balance': 20
    }
    
    keyboard = ui_service.create_subscription_keyboard(subscription_info)
    logger.info(f"✅ Клавиатура подписки создана: {len(keyboard.keyboard)} рядов кнопок")
    
    # Тест клавиатуры баланса
    keyboard = ui_service.create_balance_keyboard(20)
    logger.info(f"✅ Клавиатура баланса создана: {len(keyboard.keyboard)} рядов кнопок")
    
    # Тест форматирования сообщений
    logger.info("Тестируем форматирование сообщений...")
    
    balance_message = ui_service.format_balance_message(20, 5)
    logger.info(f"✅ Сообщение о балансе: {len(balance_message)} символов")
    
    subscription_message = ui_service.format_subscription_message(subscription_info)
    logger.info(f"✅ Сообщение о подписке: {len(subscription_message)} символов")
    
    # Тест прогресс-баров
    logger.info("Тестируем прогресс-бары...")
    
    progress_bar = ui_service.create_loading_message("Загрузка...", 3, 5)
    logger.info(f"✅ Прогресс-бар: {progress_bar}")
    
    # Тест копирования
    logger.info("Тестируем сервис копирования...")
    
    test_text = "https://example.com/vless-link"
    qr_bio = copy_service.generate_qr_code(test_text)
    if qr_bio:
        logger.info(f"✅ QR-код сгенерирован: {len(qr_bio.getvalue())} байт")
    else:
        logger.warning("❌ QR-код не сгенерирован")
    
    # Тест анимаций
    logger.info("Тестируем сервис анимаций...")
    
    # Тест прогресс-баров
    progress_bar = sticker_service.create_progress_bar(3, 5)
    logger.info(f"✅ Прогресс-бар анимации: {progress_bar}")
    
    # Тест стикеров (без бота)
    sticker_id = sticker_service.get_sticker('loading', 0)
    if sticker_id:
        logger.info(f"✅ Стикер загрузки: {sticker_id[:20]}...")
    else:
        logger.info("ℹ️ Стикеры не настроены (это нормально для теста)")
    
    logger.info("=== ТЕСТ UI СЕРВИСОВ ЗАВЕРШЕН ===")

def test_animation_sequences():
    """Тестирование анимационных последовательностей"""
    logger.info("=== ТЕСТ АНИМАЦИОННЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ ===")
    
    sticker_service = StickerService()
    
    # Тест создания анимации создания пользователя
    steps = [
        {
            'sticker': 'loading',
            'text': 'Инициализация подключения',
            'progress': {'current': 1, 'total': 5}
        },
        {
            'sticker': 'server',
            'text': 'Готовим инфраструктуру',
            'progress': {'current': 2, 'total': 5}
        },
        {
            'sticker': 'security',
            'text': 'Настраиваем протокол',
            'progress': {'current': 3, 'total': 5}
        },
        {
            'sticker': 'network',
            'text': 'Генерируем ключи',
            'progress': {'current': 4, 'total': 5}
        },
        {
            'sticker': 'success',
            'text': 'Подключение готово!',
            'progress': {'current': 5, 'total': 5}
        }
    ]
    
    logger.info(f"✅ Анимация создания пользователя: {len(steps)} шагов")
    
    # Тест создания анимации платежа
    payment_steps = [
        {
            'sticker': 'loading',
            'text': 'Обработка платежа',
            'progress': {'current': 1, 'total': 3}
        },
        {
            'sticker': 'security',
            'text': 'Проверка безопасности',
            'progress': {'current': 2, 'total': 3}
        },
        {
            'sticker': 'success',
            'text': 'Платеж успешен!',
            'progress': {'current': 3, 'total': 3}
        }
    ]
    
    logger.info(f"✅ Анимация платежа: {len(payment_steps)} шагов")
    
    # Тест создания анимации активации подписки
    activation_steps = [
        {
            'sticker': 'loading',
            'text': 'Активация подписки',
            'progress': {'current': 1, 'total': 3}
        },
        {
            'sticker': 'network',
            'text': 'Настройка доступа',
            'progress': {'current': 2, 'total': 3}
        },
        {
            'sticker': 'celebration',
            'text': 'Подписка активирована!',
            'progress': {'current': 3, 'total': 3}
        }
    ]
    
    logger.info(f"✅ Анимация активации подписки: {len(activation_steps)} шагов")
    
    logger.info("=== ТЕСТ АНИМАЦИОННЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ ЗАВЕРШЕН ===")

def test_button_grouping():
    """Тестирование группировки кнопок"""
    logger.info("=== ТЕСТ ГРУППИРОВКИ КНОПОК ===")
    
    ui_service = UIService()
    
    # Тест группировки кнопок
    button_groups = ui_service.button_groups
    
    for group_name, buttons in button_groups.items():
        logger.info(f"✅ Группа '{group_name}': {len(buttons)} кнопок")
        for button in buttons:
            emoji = ui_service.button_emojis.get(button, '❓')
            logger.info(f"   - {emoji} {button}")
    
    # Тест создания кнопок с эмодзи
    test_button = ui_service.create_button(
        "Тестовая кнопка", 
        "test_callback", 
        emoji="✅"
    )
    logger.info(f"✅ Тестовая кнопка создана: {test_button.text}")
    
    # Тест создания кнопки с цветовым индикатором
    colored_button = ui_service.create_button(
        "Подтвердить", 
        "confirm_action", 
        emoji="✅",
        color_indicator="🟢"
    )
    logger.info(f"✅ Цветная кнопка создана: {colored_button.text}")
    
    logger.info("=== ТЕСТ ГРУППИРОВКИ КНОПОК ЗАВЕРШЕН ===")

def test_interaction_feedback():
    """Тестирование обратной связи"""
    logger.info("=== ТЕСТ ОБРАТНОЙ СВЯЗИ ===")
    
    interaction_service = InteractionService()
    
    # Тест различных типов обратной связи
    feedback_types = [
        ("loading", "Загрузка..."),
        ("success", "Готово!"),
        ("error", "Ошибка!"),
        ("warning", "Внимание!"),
        ("info", "Информация")
    ]
    
    for feedback_type, message in feedback_types:
        logger.info(f"✅ Обратная связь '{feedback_type}': {message}")
    
    # Тест создания прогресс-баров
    progress_messages = [
        ("Инициализация", 1, 5),
        ("Подключение к серверу", 2, 5),
        ("Настройка протокола", 3, 5),
        ("Генерация ключей", 4, 5),
        ("Завершение", 5, 5)
    ]
    
    for text, current, total in progress_messages:
        progress_message = interaction_service.create_loading_message(
            text, current, total
        )
        logger.info(f"✅ Прогресс-сообщение: {progress_message}")
    
    logger.info("=== ТЕСТ ОБРАТНОЙ Связи ЗАВЕРШЕН ===")

if __name__ == "__main__":
    try:
        # Запускаем все тесты
        test_ui_services()
        test_animation_sequences()
        test_button_grouping()
        test_interaction_feedback()
        
        logger.info("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()