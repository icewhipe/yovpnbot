"""
Обработчики команд и сообщений
Все обработчики для команд бота, callback запросов и сообщений
"""

from .start_handler import register_start_handler
from .subscription_handler import register_subscription_handler
from .payment_handler import register_payment_handler
from .settings_handler import register_settings_handler
from .support_handler import register_support_handler
from .callback_handler import register_callback_handler
from .admin_handler import admin_router, init_admin_panel

def register_handlers(dp):
    """
    Регистрация всех обработчиков
    
    Args:
        dp: Диспетчер бота
    """
    register_start_handler(dp)
    register_subscription_handler(dp)
    register_payment_handler(dp)
    register_settings_handler(dp)
    register_support_handler(dp)
    register_callback_handler(dp)
    
    # Регистрируем админ панель
    dp.include_router(admin_router)