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
        
        # Проверяем, что сервисы созданы успешно
        if not self._services:
            logger.error("❌ Не удалось создать сервисы в middleware")
            return await handler(event, data)
        
        # Добавляем сервисы в данные события
        data["services"] = self._services
        
        # Вызываем следующий обработчик
        return await handler(event, data)
    
    async def _create_services(self, bot) -> Any:
        """
        Создать все сервисы
        
        Args:
            bot: Экземпляр бота
        
        Returns:
            BotServices: Объект с сервисами
        """
        try:
            from bot.services.bot_services import BotServices
            
            # Создаем объект сервисов
            services = BotServices(bot)
            
            logger.info("✅ Сервисы созданы в middleware")
            return services
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания сервисов в middleware: {e}")
            return None
    
    def get_user_service(self):
        """Получить сервис пользователей"""
        return self._services.get_user_service() if self._services else None
    
    def get_marzban_service(self):
        """Получить сервис Marzban"""
        return self._services.get_marzban_service() if self._services else None
    
    def get_payment_service(self):
        """Получить сервис платежей"""
        return self._services.get_payment_service() if self._services else None
    
    def get_notification_service(self):
        """Получить сервис уведомлений"""
        return self._services.get_notification_service() if self._services else None
    
    def get_animation_service(self):
        """Получить сервис анимаций"""
        return self._services.get_animation_service() if self._services else None
    
    def get_ui_service(self):
        """Получить сервис UI"""
        return self._services.get_ui_service() if self._services else None