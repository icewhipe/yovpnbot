"""
Конфигурация бота YoVPN
Центральный файл конфигурации для всех настроек бота
"""

import os
from decouple import config as decouple_config
from typing import Optional

class BotConfig:
    """
    Конфигурация бота
    
    Содержит все настройки бота, загружаемые из переменных окружения
    """
    
    def __init__(self):
        """Инициализация конфигурации"""
        self._load_config()
    
    def _load_config(self):
        """Загрузить конфигурацию из переменных окружения"""
        
        # Основные настройки бота
        self.BOT_TOKEN = decouple_config('USERBOT_TOKEN', default='')
        self.BOT_USERNAME = decouple_config('BOT_USERNAME', default='YoVPNBot')
        self.BOT_DESCRIPTION = decouple_config('BOT_DESCRIPTION', default='Современный VPN-бот с ежедневной оплатой')
        
        # Настройки Marzban
        self.MARZBAN_API_URL = decouple_config('MARZBAN_API_URL', default='')
        self.MARZBAN_ADMIN_TOKEN = decouple_config('MARZBAN_ADMIN_TOKEN', default='')
        
        # Настройки базы данных
        self.DATA_FILE = decouple_config('DATA_FILE', default='data.json')
        self.DATABASE_URL = decouple_config('DATABASE_URL', default='')
        
        # Настройки логирования
        self.LOG_LEVEL = decouple_config('LOG_LEVEL', default='INFO')
        self.LOG_FILE = decouple_config('LOG_FILE', default='bot.log')
        self.LOG_FORMAT = decouple_config('LOG_FORMAT', default='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Настройки безопасности
        self.SECRET_KEY = decouple_config('SECRET_KEY', default='your-secret-key-here')
        self.RATE_LIMIT_RPM = int(decouple_config('RATE_LIMIT_RPM', default='60'))
        self.RATE_LIMIT_RPH = int(decouple_config('RATE_LIMIT_RPH', default='1000'))
        
        # Настройки мониторинга
        self.SENTRY_DSN = decouple_config('SENTRY_DSN', default='')
        self.PROMETHEUS_PORT = int(decouple_config('PROMETHEUS_PORT', default='8000'))
        self.HEALTH_CHECK_PORT = int(decouple_config('HEALTH_CHECK_PORT', default='8080'))
        
        # Настройки Redis
        self.REDIS_URL = decouple_config('REDIS_URL', default='redis://localhost:6379')
        self.REDIS_PASSWORD = decouple_config('REDIS_PASSWORD', default='')
        
        # Настройки платежей
        self.DAILY_COST = float(decouple_config('DAILY_COST', default='4.0'))
        self.MIN_BALANCE_WARNING = float(decouple_config('MIN_BALANCE_WARNING', default='8.0'))
        self.PAYMENT_WEBHOOK_URL = decouple_config('PAYMENT_WEBHOOK_URL', default='')
        
        # Настройки уведомлений
        self.ADMIN_TELEGRAM_ID = decouple_config('ADMIN_TELEGRAM_ID', default='')
        self.NOTIFICATION_ENABLED = decouple_config('NOTIFICATION_ENABLED', default='true').lower() == 'true'
        self.NOTIFICATION_INTERVAL = int(decouple_config('NOTIFICATION_INTERVAL', default='6'))  # часы
        
        # Настройки UI
        self.DEFAULT_LANGUAGE = decouple_config('DEFAULT_LANGUAGE', default='ru')
        self.TIMEZONE = decouple_config('TIMEZONE', default='Europe/Moscow')
        
        # Настройки разработки
        self.DEBUG = decouple_config('DEBUG', default='false').lower() == 'true'
        self.DEVELOPMENT = decouple_config('DEVELOPMENT', default='false').lower() == 'true'
        
        # Настройки API
        self.API_HOST = decouple_config('API_HOST', default='0.0.0.0')
        self.API_PORT = int(decouple_config('API_PORT', default='8000'))
        self.API_PREFIX = decouple_config('API_PREFIX', default='/api/v1')
        
        # Настройки файлов
        self.UPLOAD_DIR = decouple_config('UPLOAD_DIR', default='uploads')
        self.TEMP_DIR = decouple_config('TEMP_DIR', default='temp')
        self.MAX_FILE_SIZE = int(decouple_config('MAX_FILE_SIZE', default='10485760'))  # 10MB
    
    def validate_config(self) -> bool:
        """
        Проверить конфигурацию
        
        Returns:
            bool: Валидна ли конфигурация
        """
        required_settings = [
            ('BOT_TOKEN', self.BOT_TOKEN),
            ('MARZBAN_API_URL', self.MARZBAN_API_URL),
            ('MARZBAN_ADMIN_TOKEN', self.MARZBAN_ADMIN_TOKEN)
        ]
        
        missing_settings = []
        for setting_name, setting_value in required_settings:
            if not setting_value or setting_value in ['', 'your_actual_...', 'your-secret-key-here']:
                missing_settings.append(setting_name)
        
        if missing_settings:
            print(f"❌ Отсутствуют обязательные настройки: {', '.join(missing_settings)}")
            return False
        
        return True
    
    def get_database_config(self) -> dict:
        """
        Получить конфигурацию базы данных
        
        Returns:
            dict: Конфигурация БД
        """
        return {
            'url': self.DATABASE_URL or f'sqlite:///{self.DATA_FILE}',
            'echo': self.DEBUG,
            'pool_pre_ping': True,
            'pool_recycle': 300
        }
    
    def get_redis_config(self) -> dict:
        """
        Получить конфигурацию Redis
        
        Returns:
            dict: Конфигурация Redis
        """
        return {
            'url': self.REDIS_URL,
            'password': self.REDIS_PASSWORD or None,
            'decode_responses': True,
            'socket_connect_timeout': 5,
            'socket_timeout': 5
        }
    
    def get_logging_config(self) -> dict:
        """
        Получить конфигурацию логирования
        
        Returns:
            dict: Конфигурация логирования
        """
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': self.LOG_FORMAT
                },
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': self.LOG_LEVEL,
                    'formatter': 'default'
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': self.LOG_FILE,
                    'level': self.LOG_LEVEL,
                    'formatter': 'detailed'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': self.LOG_LEVEL,
                    'propagate': False
                }
            }
        }
    
    def is_production(self) -> bool:
        """
        Проверить, работает ли бот в продакшене
        
        Returns:
            bool: Продакшен ли это
        """
        return not self.DEBUG and not self.DEVELOPMENT
    
    def is_development(self) -> bool:
        """
        Проверить, работает ли бот в режиме разработки
        
        Returns:
            bool: Разработка ли это
        """
        return self.DEVELOPMENT or self.DEBUG

# Создаем глобальный экземпляр конфигурации
config = BotConfig()

# Проверяем конфигурацию при импорте
if not config.validate_config():
    print("⚠️ Внимание: Конфигурация неполная. Проверьте переменные окружения.")