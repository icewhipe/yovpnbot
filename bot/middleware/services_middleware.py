"""
Middleware для сервисов
Добавляет сервисы в контекст бота
"""

import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)

class ServicesMiddleware(BaseMiddleware):
    """
    Middleware для добавления сервисов в контекст бота
    
    Добавляет все сервисы в bot.data для доступа из обработчиков
    """
    
    def __init__(self):
        """Инициализация middleware"""
        self._services = None
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обработка middleware
        
        Args:
            handler: Обработчик события
            event: Событие (Message или CallbackQuery)
            data: Данные события
        
        Returns:
            Any: Результат обработки
        """
        # Получаем бота из события
        bot = event.bot
        
        # Если сервисы еще не инициализированы, создаем их
        if not self._services:
            self._services = await self._create_services(bot)
        
        # Добавляем сервисы в данные события
        data["services"] = self._services
        
        # Вызываем следующий обработчик
        return await handler(event, data)
    
    async def _create_services(self, bot) -> Dict[str, Any]:
        """
        Создать все сервисы
        
        Args:
            bot: Экземпляр бота
        
        Returns:
            Dict: Словарь с сервисами
        """
        try:
            from bot.services.user_service import UserService
            from bot.services.marzban_service import MarzbanService
            from bot.services.payment_service import PaymentService
            from bot.services.notification_service import NotificationService
            from bot.services.animation_service import AnimationService
            from bot.services.ui_service import UIService
            
            # Создаем сервисы
            user_service = UserService()
            marzban_service = MarzbanService()
            payment_service = PaymentService(user_service, marzban_service)
            notification_service = NotificationService(bot)
            animation_service = AnimationService(bot)
            ui_service = UIService()
            
            services = {
                'user_service': user_service,
                'marzban_service': marzban_service,
                'payment_service': payment_service,
                'notification_service': notification_service,
                'animation_service': animation_service,
                'ui_service': ui_service
            }
            
            logger.info("✅ Сервисы созданы в middleware")
            return services
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания сервисов в middleware: {e}")
            return {}
    
    def get_user_service(self):
        """Получить сервис пользователей"""
        return self._services.get('user_service') if self._services else None
    
    def get_marzban_service(self):
        """Получить сервис Marzban"""
        return self._services.get('marzban_service') if self._services else None
    
    def get_payment_service(self):
        """Получить сервис платежей"""
        return self._services.get('payment_service') if self._services else None
    
    def get_notification_service(self):
        """Получить сервис уведомлений"""
        return self._services.get('notification_service') if self._services else None
    
    def get_animation_service(self):
        """Получить сервис анимаций"""
        return self._services.get('animation_service') if self._services else None
    
    def get_ui_service(self):
        """Получить сервис UI"""
        return self._services.get('ui_service') if self._services else None