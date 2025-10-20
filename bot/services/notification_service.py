"""
Сервис уведомлений
Отправка уведомлений пользователям о платежах, подписках и важных событиях
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Сервис для отправки уведомлений
    
    Отвечает за:
    - Уведомления о платежах и подписках
    - Предупреждения о низком балансе
    - Системные уведомления
    - Массовые рассылки
    """
    
    def __init__(self, bot):
        """
        Инициализация сервиса
        
        Args:
            bot: Экземпляр бота
        """
        self.bot = bot
        self._running = False
        
        logger.info("✅ NotificationService инициализирован")
    
    async def send_payment_success_notification(self, user_id: int, amount: float, days: int):
        """
        Отправить уведомление об успешной оплате
        
        Args:
            user_id: ID пользователя
            amount: Сумма платежа
            days: Количество дней
        """
        try:
            message = f"""
💰 <b>Платеж успешно обработан!</b>

✅ <b>Сумма:</b> {amount:.2f} ₽
📅 <b>Добавлено дней:</b> {days}
💳 <b>Статус:</b> Подтвержден

<b>Ваш баланс пополнен!</b>
Теперь вы можете активировать подписку или продолжить использование VPN.
            """
            
            await self.bot.send_message(user_id, message)
            logger.info(f"📧 Уведомление об оплате отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки уведомления об оплате: {e}")
    
    async def send_subscription_activated_notification(self, user_id: int, days: int):
        """
        Отправить уведомление об активации подписки
        
        Args:
            user_id: ID пользователя
            days: Количество дней подписки
        """
        try:
            message = f"""
🎉 <b>Подписка активирована!</b>

✅ <b>Статус:</b> Активна
📅 <b>Срок:</b> {days} дней
💰 <b>Стоимость:</b> 4 ₽ в день
🔄 <b>Продление:</b> Автоматическое

<b>Следующие шаги:</b>
1. 📱 Настройте VPN на устройстве
2. 🔗 Скопируйте конфигурацию
3. 🚀 Наслаждайтесь безопасным интернетом!
            """
            
            await self.bot.send_message(user_id, message)
            logger.info(f"📧 Уведомление об активации подписки отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки уведомления об активации: {e}")
    
    async def send_low_balance_warning(self, user_id: int, balance: float, days_left: int):
        """
        Отправить предупреждение о низком балансе
        
        Args:
            user_id: ID пользователя
            balance: Текущий баланс
            days_left: Дней осталось
        """
        try:
            message = f"""
⚠️ <b>Внимание! Низкий баланс</b>

💰 <b>Текущий баланс:</b> {balance:.2f} ₽
📅 <b>Дней осталось:</b> {days_left}
🔄 <b>Продление:</b> Автоматическое

<b>Рекомендуем пополнить баланс</b> для непрерывного доступа к VPN.

<b>Что произойдет:</b>
• При балансе < 4 ₽ подписка приостановится
• Вы получите уведомление о приостановке
• После пополнения подписка возобновится автоматически
            """
            
            await self.bot.send_message(user_id, message)
            logger.info(f"📧 Предупреждение о низком балансе отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки предупреждения о балансе: {e}")
    
    async def send_subscription_suspended_notification(self, user_id: int, reason: str = "Недостаточно средств"):
        """
        Отправить уведомление о приостановке подписки
        
        Args:
            user_id: ID пользователя
            reason: Причина приостановки
        """
        try:
            message = f"""
❌ <b>Подписка приостановлена</b>

📋 <b>Причина:</b> {reason}
🔄 <b>Возобновление:</b> После пополнения баланса
💳 <b>Стоимость:</b> 4 ₽ в день

<b>Для возобновления подписки:</b>
1. 💰 Пополните баланс на сумму от 4 ₽
2. 🔄 Подписка активируется автоматически
3. 📱 Настройте VPN на устройстве

<b>Нужна помощь?</b> Обратитесь в поддержку 👇
            """
            
            await self.bot.send_message(user_id, message)
            logger.info(f"📧 Уведомление о приостановке подписки отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки уведомления о приостановке: {e}")
    
    async def send_daily_payment_notification(self, user_id: int, amount: float, days_left: int):
        """
        Отправить уведомление о ежедневном списании
        
        Args:
            user_id: ID пользователя
            amount: Сумма списания
            days_left: Дней осталось
        """
        try:
            message = f"""
💳 <b>Ежедневное списание</b>

💰 <b>Списано:</b> {amount:.2f} ₽
📅 <b>Дней осталось:</b> {days_left}
🔄 <b>Следующее списание:</b> Завтра в 00:00

<b>Ваша подписка продлена на 1 день!</b>
Продолжайте наслаждаться безопасным интернетом.
            """
            
            await self.bot.send_message(user_id, message)
            logger.info(f"📧 Уведомление о ежедневном списании отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки уведомления о списании: {e}")
    
    async def send_system_notification(self, user_id: int, title: str, message: str, notification_type: str = "info"):
        """
        Отправить системное уведомление
        
        Args:
            user_id: ID пользователя
            title: Заголовок уведомления
            message: Текст уведомления
            notification_type: Тип уведомления (info, warning, error, success)
        """
        try:
            emoji_map = {
                'info': 'ℹ️',
                'warning': '⚠️',
                'error': '❌',
                'success': '✅'
            }
            
            emoji = emoji_map.get(notification_type, 'ℹ️')
            
            formatted_message = f"""
{emoji} <b>{title}</b>

{message}

<b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
            """
            
            await self.bot.send_message(user_id, formatted_message)
            logger.info(f"📧 Системное уведомление отправлено пользователю {user_id}: {title}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки системного уведомления: {e}")
    
    async def notification_loop(self):
        """
        Основной цикл уведомлений
        Проверяет пользователей и отправляет уведомления
        """
        self._running = True
        logger.info("🔄 Запуск цикла уведомлений")
        
        while self._running:
            try:
                await self._check_and_send_notifications()
                # Проверяем каждые 6 часов
                await asyncio.sleep(6 * 60 * 60)
            except Exception as e:
                logger.error(f"❌ Ошибка в цикле уведомлений: {e}")
                await asyncio.sleep(60 * 60)  # Ждем час при ошибке
    
    async def _check_and_send_notifications(self):
        """
        Проверить пользователей и отправить необходимые уведомления
        """
        try:
            # Здесь была бы проверка всех пользователей
            # и отправка уведомлений о низком балансе
            logger.debug("🔍 Проверка пользователей для уведомлений")
            
        except Exception as e:
            logger.error(f"❌ Ошибка проверки уведомлений: {e}")
    
    async def send_bulk_notification(self, user_ids: List[int], message: str, title: str = "Уведомление"):
        """
        Отправить массовое уведомление
        
        Args:
            user_ids: Список ID пользователей
            message: Текст сообщения
            title: Заголовок сообщения
        """
        try:
            formatted_message = f"""
📢 <b>{title}</b>

{message}

<b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
            """
            
            success_count = 0
            for user_id in user_ids:
                try:
                    await self.bot.send_message(user_id, formatted_message)
                    success_count += 1
                except Exception as e:
                    logger.error(f"❌ Ошибка отправки уведомления пользователю {user_id}: {e}")
            
            logger.info(f"📧 Массовое уведомление отправлено: {success_count}/{len(user_ids)}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка массовой рассылки: {e}")
    
    async def stop(self):
        """Остановить сервис"""
        self._running = False
        logger.info("🛑 NotificationService остановлен")
    
    def is_running(self) -> bool:
        """Проверить, запущен ли сервис"""
        return self._running