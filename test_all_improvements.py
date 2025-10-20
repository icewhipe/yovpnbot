#!/usr/bin/env python3
"""
Комплексное тестирование всех улучшений бота
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, List
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImprovementTester:
    """Тестер улучшений бота"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
    
    async def test_immediate_response(self):
        """Тест немедленного отклика"""
        logger.info("=== ТЕСТ НЕМЕДЛЕННОГО ОТКЛИКА ===")
        
        try:
            from src.services.ux_service import UXService
            
            ux_service = UXService()
            
            # Тест генерации emoji
            success_emoji = ux_service.get_random_emoji(ux_service.ResponseType.SUCCESS)
            error_emoji = ux_service.get_random_emoji(ux_service.ResponseType.ERROR)
            
            assert success_emoji in ux_service.emoji_fallbacks[ux_service.ResponseType.SUCCESS]
            assert error_emoji in ux_service.emoji_fallbacks[ux_service.ResponseType.ERROR]
            
            # Тест создания прогресс-бара
            progress_bar = ux_service.create_progress_bar(75, 10)
            expected_bar = "████████░░"  # 8 filled, 2 empty
            assert progress_bar == expected_bar
            
            # Тест маскирования данных
            sensitive_data = "password=secret123 token=abc123"
            masked = ux_service.mask_sensitive_data(sensitive_data)
            assert "secret123" not in masked
            assert "abc123" not in masked
            
            self.test_results['immediate_response'] = True
            logger.info("✅ Тест немедленного отклика - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест немедленного отклика - ОШИБКА: {e}")
            self.test_results['immediate_response'] = False
    
    async def test_validation_service(self):
        """Тест сервиса валидации"""
        logger.info("=== ТЕСТ ВАЛИДАЦИИ ДАННЫХ ===")
        
        try:
            from src.services.validation_service import ValidationService, ValidationError
            
            validation_service = ValidationService()
            
            # Тест валидации платежа
            valid_payment = {
                'amount': 20,
                'payment_method': 'card',
                'user_id': 12345
            }
            
            validated_payment = validation_service.validate_payment_request(valid_payment)
            assert validated_payment.amount == 20
            assert validated_payment.user_id == 12345
            
            # Тест валидации с ошибкой
            invalid_payment = {
                'amount': 3,  # Меньше минимума
                'payment_method': 'card',
                'user_id': 12345
            }
            
            try:
                validation_service.validate_payment_request(invalid_payment)
                assert False, "Должна была быть ошибка валидации"
            except ValidationError:
                pass  # Ожидаемая ошибка
            
            # Тест очистки строки
            dirty_string = "<script>alert('xss')</script>Hello World"
            clean_string = validation_service.sanitize_string(dirty_string)
            assert "<script>" not in clean_string
            assert "Hello World" in clean_string
            
            # Тест валидации пути файла
            safe_path = "config/user123.json"
            dangerous_path = "../../../etc/passwd"
            
            assert validation_service.validate_file_path(safe_path) == True
            assert validation_service.validate_file_path(dangerous_path) == False
            
            self.test_results['validation'] = True
            logger.info("✅ Тест валидации данных - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест валидации данных - ОШИБКА: {e}")
            self.test_results['validation'] = False
    
    async def test_security_service(self):
        """Тест сервиса безопасности"""
        logger.info("=== ТЕСТ БЕЗОПАСНОСТИ ===")
        
        try:
            from src.services.security_service import SecurityService
            
            security_service = SecurityService()
            
            # Тест маскирования чувствительных данных
            sensitive_text = "password=secret123 api_key=sk-1234567890abcdef"
            masked = security_service.mask_sensitive_data(sensitive_text)
            assert "secret123" not in masked
            assert "sk-1234567890abcdef" not in masked
            
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
            assert len(token1) == 32
            assert token1 != token2
            
            # Тест хеширования паролей
            password = "test_password"
            hashed = security_service.hash_password(password)
            assert security_service.verify_password(password, hashed) == True
            assert security_service.verify_password("wrong_password", hashed) == False
            
            # Тест HMAC подписи
            data = "test_data"
            signature = security_service.generate_hmac_signature(data)
            assert security_service.verify_hmac_signature(data, signature) == True
            assert security_service.verify_hmac_signature("wrong_data", signature) == False
            
            self.test_results['security'] = True
            logger.info("✅ Тест безопасности - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест безопасности - ОШИБКА: {e}")
            self.test_results['security'] = False
    
    async def test_async_architecture(self):
        """Тест асинхронной архитектуры"""
        logger.info("=== ТЕСТ АСИНХРОННОЙ АРХИТЕКТУРЫ ===")
        
        try:
            # Тест импорта асинхронных модулей
            from src.bot.async_bot import AsyncYoVPNBot, BotStates
            from src.config.monitoring import MonitoringConfig, SecurityConfig
            
            # Тест создания конфигурации
            monitoring_config = MonitoringConfig.from_env()
            security_config = SecurityConfig.from_env()
            
            assert monitoring_config.log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']
            assert len(security_config.secret_key) >= 32
            
            # Тест FSM состояний
            assert hasattr(BotStates, 'waiting_for_payment_amount')
            assert hasattr(BotStates, 'waiting_for_payment_method')
            
            self.test_results['async_architecture'] = True
            logger.info("✅ Тест асинхронной архитектуры - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест асинхронной архитектуры - ОШИБКА: {e}")
            self.test_results['async_architecture'] = False
    
    async def test_performance_improvements(self):
        """Тест улучшений производительности"""
        logger.info("=== ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ ===")
        
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
            
            self.test_results['performance'] = True
            logger.info("✅ Тест производительности - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест производительности - ОШИБКА: {e}")
            self.test_results['performance'] = False
    
    async def test_error_handling(self):
        """Тест обработки ошибок"""
        logger.info("=== ТЕСТ ОБРАБОТКИ ОШИБОК ===")
        
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
            
            self.test_results['error_handling'] = True
            logger.info("✅ Тест обработки ошибок - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест обработки ошибок - ОШИБКА: {e}")
            self.test_results['error_handling'] = False
    
    async def test_monitoring_setup(self):
        """Тест настройки мониторинга"""
        logger.info("=== ТЕСТ МОНИТОРИНГА ===")
        
        try:
            from src.config.monitoring import setup_logging, setup_sentry, setup_prometheus
            
            # Тест настройки логирования
            from src.config.monitoring import MonitoringConfig
            config = MonitoringConfig()
            setup_logging(config)
            
            # Тест настройки Sentry (без DSN)
            setup_sentry(config)
            
            # Тест настройки Prometheus
            metrics = setup_prometheus(config)
            # Может быть None если Prometheus не установлен
            
            self.test_results['monitoring'] = True
            logger.info("✅ Тест мониторинга - ПРОЙДЕН")
            
        except Exception as e:
            logger.error(f"❌ Тест мониторинга - ОШИБКА: {e}")
            self.test_results['monitoring'] = False
    
    async def run_all_tests(self):
        """Запуск всех тестов"""
        logger.info("🚀 Запуск комплексного тестирования улучшений...")
        
        tests = [
            self.test_immediate_response,
            self.test_validation_service,
            self.test_security_service,
            self.test_async_architecture,
            self.test_performance_improvements,
            self.test_error_handling,
            self.test_monitoring_setup
        ]
        
        for test in tests:
            try:
                await test()
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
        
        with open('test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info("📄 Отчет сохранен в test_report.json")

async def main():
    """Главная функция"""
    tester = ImprovementTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())