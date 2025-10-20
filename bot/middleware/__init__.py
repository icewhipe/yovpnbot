"""
Middleware для бота
Промежуточное ПО для обработки запросов
"""

from .services_middleware import ServicesMiddleware
from .logging_middleware import LoggingMiddleware

def register_middleware(dp):
    """
    Регистрация всех middleware
    
    Args:
        dp: Диспетчер бота
    """
    # Добавляем middleware для сервисов
    dp.message.middleware(ServicesMiddleware())
    dp.callback_query.middleware(ServicesMiddleware())
    
    # Добавляем middleware для логирования
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())