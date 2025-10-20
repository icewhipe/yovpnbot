#!/usr/bin/env python3
"""
Сервис для отправки уведомлений пользователям
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class NotificationService:
    """Сервис для отправки уведомлений пользователям"""
    
    def __init__(self, bot=None):
        self.bot = bot
        self.daily_cost = 4  # Стоимость дня в рублях
    
    def set_bot(self, bot):
        """Установить экземпляр бота для отправки сообщений"""
        self.bot = bot
    
    def send_payment_notification(self, telegram_id: int, amount: float, balance: float, action: str):
        """Отправить уведомление о платеже"""
        if not self.bot:
            logger.warning("Бот не установлен, уведомление не отправлено")
            return False
        
        try:
            if action == 'charged':
                text = f"""
💳 <b>Списание средств</b>

С вашего баланса списано: <b>{amount} ₽</b>
Текущий баланс: <b>{balance} ₽</b>

Ваша подписка продлена на 1 день.
Доступ к VPN активен до завтра.
"""
            elif action == 'suspended':
                text = f"""
⚠️ <b>Подписка приостановлена</b>

Недостаточно средств для продления подписки.
Текущий баланс: <b>{balance} ₽</b>
Требуется: <b>{self.daily_cost} ₽</b> в день

Для возобновления подписки пополните баланс.
"""
            else:
                return False
            
            self.bot.send_message(
                chat_id=telegram_id,
                text=text,
                parse_mode='HTML'
            )
            
            logger.info(f"Уведомление о платеже отправлено пользователю {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления о платеже для {telegram_id}: {e}")
            return False
    
    def send_low_balance_notification(self, telegram_id: int, balance: float):
        """Отправить уведомление о низком балансе"""
        if not self.bot:
            logger.warning("Бот не установлен, уведомление не отправлено")
            return False
        
        try:
            days_remaining = int(balance / self.daily_cost)
            
            if days_remaining == 0:
                text = f"""
🚨 <b>Критически низкий баланс!</b>

Ваш баланс: <b>{balance} ₽</b>
Подписка будет приостановлена завтра!

Пополните баланс прямо сейчас, чтобы не потерять доступ к VPN.
"""
            elif days_remaining == 1:
                text = f"""
⚠️ <b>Низкий баланс</b>

Ваш баланс: <b>{balance} ₽</b>
Осталось дней: <b>{days_remaining}</b>

Рекомендуем пополнить баланс, чтобы не потерять доступ к VPN.
"""
            else:
                text = f"""
💡 <b>Напоминание о балансе</b>

Ваш баланс: <b>{balance} ₽</b>
Осталось дней: <b>{days_remaining}</b>

Пополните баланс заранее для бесперебойной работы VPN.
"""
            
            self.bot.send_message(
                chat_id=telegram_id,
                text=text,
                parse_mode='HTML'
            )
            
            logger.info(f"Уведомление о низком балансе отправлено пользователю {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления о низком балансе для {telegram_id}: {e}")
            return False
    
    def send_subscription_reactivated_notification(self, telegram_id: int, balance: float):
        """Отправить уведомление о возобновлении подписки"""
        if not self.bot:
            logger.warning("Бот не установлен, уведомление не отправлено")
            return False
        
        try:
            text = f"""
✅ <b>Подписка возобновлена!</b>

Ваш баланс пополнен: <b>{balance} ₽</b>
Подписка автоматически активирована.

Добро пожаловать обратно! 🎉
"""
            
            self.bot.send_message(
                chat_id=telegram_id,
                text=text,
                parse_mode='HTML'
            )
            
            logger.info(f"Уведомление о возобновлении подписки отправлено пользователю {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления о возобновлении подписки для {telegram_id}: {e}")
            return False
    
    def send_welcome_bonus_notification(self, telegram_id: int, bonus_amount: float, balance: float):
        """Отправить уведомление о приветственном бонусе"""
        if not self.bot:
            logger.warning("Бот не установлен, уведомление не отправлено")
            return False
        
        try:
            days = int(balance / self.daily_cost)
            
            text = f"""
🎉 <b>Добро пожаловать!</b>

Вам начислен приветственный бонус: <b>{bonus_amount} ₽</b>
Текущий баланс: <b>{balance} ₽</b>
Доступно дней: <b>{days}</b>

Ваша подписка активирована на {days} дней.
Наслаждайтесь быстрым и безопасным VPN! 🚀
"""
            
            self.bot.send_message(
                chat_id=telegram_id,
                text=text,
                parse_mode='HTML'
            )
            
            logger.info(f"Уведомление о приветственном бонусе отправлено пользователю {telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления о приветственном бонусе для {telegram_id}: {e}")
            return False