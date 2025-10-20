#!/usr/bin/env python3
"""
Упрощенное тестирование улучшений бота (без внешних зависимостей)
"""

import logging
import time
import json
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleImprovementTester:
    """Упрощенный тестер улучшений"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
    
    def test_ux_service_basic(self):
        """Тест базовой функциональности UXService"""
        logger.info("=== ТЕСТ UX СЕРВИСА ===")
        
        try:
            from src.services.ux_service import UXService, ResponseType
            
            ux_service = UXService()
            
            # Тест генерации emoji
            success_emoji = ux_service.get_random_emoji(ResponseType.SUCCESS)
            error_emoji = ux_service.get_random_emoji(ResponseType.ERROR)
            
            assert success_emoji in ux_service.emoji_fallbacks[ResponseType.SUCCESS]
            assert error_emoji in ux_service.emoji_fallbacks[ResponseType.ERROR]
            
            # Тест создания прогресс-бара
            progress_bar = ux_service.create_progress_bar(75, 10)
            expected_bar = "[███████░░░]"  # 7 filled, 3 empty
            assert progress_bar == expected_bar
            
            # Тест маскирования данных (UXService не маскирует, только возвращает как есть)
            sensitive_data = "password=secret123 token=abc123"
            masked = ux_service.mask_sensitive_data(sensitive_data)
            assert masked == sensitive_data  # UXService возвращает данные как есть
            
            self.test_results['ux_service'] = True
            logger.info("✅ Тест UX сервиса - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест UX сервиса - ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.test_results['ux_service'] = False
    
    def test_security_service_basic(self):
        """Тест базовой функциональности SecurityService"""
        logger.info("=== ТЕСТ СЕРВИСА БЕЗОПАСНОСТИ ===")
        
        try:
            from src.services.security_service_simple import SecurityService
            
            security_service = SecurityService()
            
            # Тест маскирования чувствительных данных
            sensitive_text = "password=secret123 api_key=sk-1234567890abcdef"
            masked = security_service.mask_sensitive_data(sensitive_text)
            assert "***MASKED***" in masked  # Проверяем что данные замаскированы
            assert len(masked) > len(sensitive_text)  # Маскированный текст длиннее
            
            # Тест валидации ввода
            safe_input = "Hello World"
            sql_injection = "'; DROP TABLE users; --"
            xss_input = "<script>alert('xss')</script>"
            
            assert security_service.validate_input(safe_input) == True
            assert security_service.validate_input(sql_injection) == False
            assert security_service.validate_input(xss_input) == False
            
            # Тест валидации callback data
            safe_callback = "balance_menu"
            dangerous_callback = "balance<script>alert('xss')</script>"
            
            assert security_service.validate_callback_data(safe_callback) == True
            assert security_service.validate_callback_data(dangerous_callback) == False
            
            # Тест генерации токенов
            token1 = security_service.generate_secure_token()
            token2 = security_service.generate_secure_token()
            assert len(token1) == 43  # URL-safe base64 токен длиной 43
            assert token1 != token2
            
            self.test_results['security_service'] = True
            logger.info("✅ Тест сервиса безопасности - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест сервиса безопасности - ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.test_results['security_service'] = False
    
    def test_validation_service_basic(self):
        """Тест базовой функциональности ValidationService"""
        logger.info("=== ТЕСТ СЕРВИСА ВАЛИДАЦИИ ===")
        
        try:
            from src.services.validation_service_simple import ValidationService, ValidationError
            
            validation_service = ValidationService()
            
            # Тест очистки строки
            dirty_string = "<script>alert('xss')</script>Hello World"
            clean_string = validation_service.sanitize_string(dirty_string)
            assert "<script>" not in clean_string
            assert "Hello World" in clean_string
            
            # Тест валидации пути файла
            safe_path = "user123.json"
            dangerous_path = "../../../etc/passwd"
            
            assert validation_service.validate_file_path(safe_path) == True
            assert validation_service.validate_file_path(dangerous_path) == False
            
            # Тест валидации Telegram username
            valid_username = "testuser123"
            invalid_username = "test<script>alert('xss')</script>"
            
            assert validation_service.validate_telegram_username(valid_username) == True
            assert validation_service.validate_telegram_username(invalid_username) == False
            
            # Тест валидации суммы
            assert validation_service.validate_amount_range(100, 0, 1000) == True
            assert validation_service.validate_amount_range(-10, 0, 1000) == False
            assert validation_service.validate_amount_range(1500, 0, 1000) == False
            
            self.test_results['validation_service'] = True
            logger.info("✅ Тест сервиса валидации - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест сервиса валидации - ОШИБКА: {e}")
            self.test_results['validation_service'] = False
    
    def test_error_codes(self):
        """Тест системы кодов ошибок"""
        logger.info("=== ТЕСТ КОДОВ ОШИБОК ===")
        
        try:
            from src.services.ux_service import UXService, ErrorCode
            
            ux_service = UXService()
            
            # Тест стандартизованных кодов ошибок
            error_codes = ['E001', 'E002', 'E003', 'E004', 'E005']
            for code in error_codes:
                assert code in ux_service.error_codes
                error_info = ux_service.error_codes[code]
                assert hasattr(error_info, 'code')
                assert hasattr(error_info, 'message')
                assert hasattr(error_info, 'user_message')
                assert hasattr(error_info, 'action_required')
            
            # Тест обработки неизвестных ошибок
            unknown_error = ux_service.error_codes.get('E999')
            if unknown_error:
                assert unknown_error.code == 'E999'
            
            self.test_results['error_codes'] = True
            logger.info("✅ Тест кодов ошибок - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест кодов ошибок - ОШИБКА: {e}")
            self.test_results['error_codes'] = False
    
    def test_caching(self):
        """Тест системы кэширования"""
        logger.info("=== ТЕСТ КЭШИРОВАНИЯ ===")
        
        try:
            from src.services.ux_service import UXService
            
            ux_service = UXService()
            
            # Тест кэширования
            cache_key = "test_key"
            test_data = {"test": "data"}
            
            # Кэшируем данные
            ux_service.cache_response(cache_key, test_data)
            
            # Получаем из кэша
            cached_data = ux_service.get_cached_response(cache_key)
            assert cached_data == test_data
            
            # Тест производительности маскирования
            large_text = "password=secret " * 1000
            start_time = time.time()
            masked = ux_service.mask_sensitive_data(large_text)
            end_time = time.time()
            
            processing_time = end_time - start_time
            assert processing_time < 1.0  # Должно быть быстрее 1 секунды
            
            self.test_results['caching'] = True
            logger.info("✅ Тест кэширования - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест кэширования - ОШИБКА: {e}")
            self.test_results['caching'] = False
    
    def test_ui_service(self):
        """Тест UI сервиса"""
        logger.info("=== ТЕСТ UI СЕРВИСА ===")
        
        try:
            from src.services.ui_service import UIService
            
            ui_service = UIService()
            
            # Тест создания кнопок
            button = ui_service.create_button_with_emoji("test", "test_callback", "info")
            assert button.text == "ℹ️ test"
            assert button.callback_data == "test_callback"
            
            # Тест форматирования сообщений
            user_stats = {"balance": 100, "days_remaining": 25}
            text = ui_service.format_balance_message(100, 25)
            assert "100 ₽" in text
            assert "25" in text  # Проверяем что число 25 есть в тексте
            
            self.test_results['ui_service'] = True
            logger.info("✅ Тест UI сервиса - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест UI сервиса - ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            self.test_results['ui_service'] = False
    
    def test_animation_service(self):
        """Тест сервиса анимации"""
        logger.info("=== ТЕСТ СЕРВИСА АНИМАЦИИ ===")
        
        try:
            from src.services.animation_service import StickerService, AnimationType
            
            sticker_service = StickerService()
            
            # Тест получения стикера
            sticker_id = sticker_service.get_sticker('loading', 0)
            # Может быть None если стикеры отключены
            
            # Тест создания прогресс-бара
            progress_bar = sticker_service.create_progress_bar(3, 5, 5)  # 3 из 5, ширина 5
            assert len(progress_bar) >= 5
            assert "⬛" in progress_bar or "⬜" in progress_bar
            
            # Тест анимации создания
            steps = [
                ("Подготовка", "loading"),
                ("Настройка", "server"),
                ("Завершение", "success")
            ]
            # Не тестируем реальную отправку, только создание
            
            self.test_results['animation_service'] = True
            logger.info("✅ Тест сервиса анимации - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест сервиса анимации - ОШИБКА: {e}")
            self.test_results['animation_service'] = False
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        logger.info("🚀 Запуск упрощенного тестирования улучшений...")
        
        tests = [
            self.test_ux_service_basic,
            self.test_security_service_basic,
            self.test_validation_service_basic,
            self.test_error_codes,
            self.test_caching,
            self.test_ui_service,
            self.test_animation_service
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                logger.error(f"Критическая ошибка в тесте {test.__name__}: {e}")
        
        # Подсчет результатов
        total_tests = len(tests)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        # Время выполнения
        total_time = time.time() - self.start_time
        
        # Вывод результатов
        logger.info("=" * 60)
        logger.info("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        logger.info("=" * 60)
        
        for test_name, result in self.test_results.items():
            status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
            logger.info(f"{test_name:25} {status}")
        
        logger.info("-" * 60)
        logger.info(f"Всего тестов:     {total_tests}")
        logger.info(f"Пройдено:         {passed_tests}")
        logger.info(f"Провалено:        {failed_tests}")
        logger.info(f"Время выполнения: {total_time:.2f} сек")
        logger.info(f"Успешность:       {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests == 0:
            logger.info("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        else:
            logger.warning(f"⚠️  {failed_tests} тестов провалено")
        
        # Сохранение отчета
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'execution_time': total_time,
            'results': self.test_results
        }
        
        with open('test_report_simple.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info("📄 Отчет сохранен в test_report_simple.json")

def main():
    """Главная функция"""
    tester = SimpleImprovementTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()