"""
Конфигурация бота
"""

import os
from decouple import config as decouple_config

# Основные настройки бота
BOT_TOKEN = decouple_config('USERBOT_TOKEN', default='')
MARZBAN_API_URL = decouple_config('MARZBAN_API_URL', default='')
MARZBAN_ADMIN_TOKEN = decouple_config('MARZBAN_ADMIN_TOKEN', default='')

# Настройки базы данных
DATA_FILE = decouple_config('DATA_FILE', default='data.json')

# Настройки логирования
LOG_LEVEL = decouple_config('LOG_LEVEL', default='INFO')
LOG_FILE = decouple_config('LOG_FILE', default='bot.log')

# Настройки безопасности
SECRET_KEY = decouple_config('SECRET_KEY', default='your-secret-key-here')
RATE_LIMIT_RPM = int(decouple_config('RATE_LIMIT_RPM', default='60'))
RATE_LIMIT_RPH = int(decouple_config('RATE_LIMIT_RPH', default='1000'))

# Настройки мониторинга
SENTRY_DSN = decouple_config('SENTRY_DSN', default='')
PROMETHEUS_PORT = int(decouple_config('PROMETHEUS_PORT', default='8000'))

# Настройки Redis
REDIS_URL = decouple_config('REDIS_URL', default='redis://localhost:6379')

# Настройки платежей
DAILY_COST = float(decouple_config('DAILY_COST', default='4.0'))
MIN_BALANCE_WARNING = float(decouple_config('MIN_BALANCE_WARNING', default='8.0'))

# Настройки уведомлений
ADMIN_TELEGRAM_ID = decouple_config('ADMIN_TELEGRAM_ID', default='')
NOTIFICATION_ENABLED = decouple_config('NOTIFICATION_ENABLED', default='true').lower() == 'true'

# Проверка обязательных настроек
def validate_config():
    """Проверка конфигурации"""
    required_settings = {
        'BOT_TOKEN': BOT_TOKEN,
        'MARZBAN_API_URL': MARZBAN_API_URL,
        'MARZBAN_ADMIN_TOKEN': MARZBAN_ADMIN_TOKEN
    }
    
    missing_settings = []
    for setting, value in required_settings.items():
        if not value or value == 'your_actual_...':
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Отсутствуют обязательные настройки: {', '.join(missing_settings)}")
    
    return True

# Создаем объект конфигурации для обратной совместимости
class Config:
    def __init__(self):
        self.BOT_TOKEN = BOT_TOKEN
        self.MARZBAN_API_URL = MARZBAN_API_URL
        self.MARZBAN_ADMIN_TOKEN = MARZBAN_ADMIN_TOKEN
        self.DATA_FILE = DATA_FILE
        self.LOG_LEVEL = LOG_LEVEL
        self.LOG_FILE = LOG_FILE
        self.SECRET_KEY = SECRET_KEY
        self.RATE_LIMIT_RPM = RATE_LIMIT_RPM
        self.RATE_LIMIT_RPH = RATE_LIMIT_RPH
        self.SENTRY_DSN = SENTRY_DSN
        self.PROMETHEUS_PORT = PROMETHEUS_PORT
        self.REDIS_URL = REDIS_URL
        self.DAILY_COST = DAILY_COST
        self.MIN_BALANCE_WARNING = MIN_BALANCE_WARNING
        self.ADMIN_TELEGRAM_ID = ADMIN_TELEGRAM_ID
        self.NOTIFICATION_ENABLED = NOTIFICATION_ENABLED

# Создаем экземпляр конфигурации
config = Config()