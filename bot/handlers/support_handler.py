"""
Обработчик поддержки
Управление обращениями в поддержку и FAQ
"""

import logging
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram import F

from assets.emojis.interface import EMOJI

logger = logging.getLogger(__name__)

async def handle_support(callback: CallbackQuery):
    """
    Обработчик кнопки "Поддержка"
    
    Показывает меню поддержки и FAQ
    """
    user_id = callback.from_user.id
    
    try:
        message_text = f"""
🆘 <b>Поддержка YoVPN</b>

<b>Мы всегда готовы помочь!</b>

<b>📞 Способы связи:</b>
• 💬 Telegram: @YoVPNSupport
• 📧 Email: support@yovpn.com
• 🌐 Сайт: https://yovpn.com/support

<b>⏰ Время работы:</b>
• Понедельник - Пятница: 9:00 - 21:00
• Суббота - Воскресенье: 10:00 - 18:00
• Экстренная поддержка: 24/7

<b>🔍 Частые вопросы:</b>
• Как настроить VPN?
• Как пополнить баланс?
• Почему не работает подключение?
• Как отменить подписку?

<b>📋 Перед обращением:</b>
• Проверьте FAQ ниже
• Укажите ваш ID: {user_id}
• Опишите проблему подробно
        """
        
        from bot.services.ui_service import UIService
        ui_service = UIService()
        
        # Создаем клавиатуру поддержки
        keyboard = ui_service.create_navigation_keyboard([
            {
                'text': f"{EMOJI['info']} FAQ",
                'callback_data': 'faq'
            },
            {
                'text': f"{EMOJI['message']} Написать в поддержку",
                'callback_data': 'contact_support'
            },
            {
                'text': f"{EMOJI['back']} Назад",
                'callback_data': 'main_menu'
            }
        ])
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        logger.info(f"🆘 Показана поддержка для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_support: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

async def handle_faq(callback: CallbackQuery):
    """
    Обработчик FAQ
    
    Показывает часто задаваемые вопросы
    """
    try:
        message_text = f"""
❓ <b>Часто задаваемые вопросы</b>

<b>🔧 Настройка VPN:</b>
<b>Q:</b> Как настроить VPN на телефоне?
<b>A:</b> Скачайте V2rayNG (Android) или OneClick (iOS), скопируйте ссылку из бота и подключитесь.

<b>Q:</b> Как настроить VPN на компьютере?
<b>A:</b> Скачайте V2rayN (Windows), V2rayU (macOS) или v2ray-core (Linux), вставьте ссылку и подключитесь.

<b>💰 Платежи и баланс:</b>
<b>Q:</b> Как пополнить баланс?
<b>A:</b> Нажмите "Пополнить" в главном меню, выберите сумму и способ оплаты.

<b>Q:</b> Сколько стоит подписка?
<b>A:</b> 4 рубля в день. Списание происходит автоматически каждый день в 00:00.

<b>Q:</b> Что происходит при недостатке средств?
<b>A:</b> Подписка приостанавливается. После пополнения баланса она возобновится автоматически.

<b>🔒 Безопасность:</b>
<b>Q:</b> Безопасен ли ваш VPN?
<b>A:</b> Да, мы используем современные протоколы шифрования и не ведем логи активности.

<b>Q:</b> Можно ли использовать на нескольких устройствах?
<b>A:</b> Да, одну подписку можно использовать на неограниченном количестве устройств.

<b>🔄 Технические вопросы:</b>
<b>Q:</b> Почему не работает подключение?
<b>A:</b> Проверьте интернет-соединение, обновите приложение или попробуйте другой сервер.

<b>Q:</b> Как отменить подписку?
<b>A:</b> Просто не пополняйте баланс. Подписка автоматически приостановится при недостатке средств.
        """
        
        from bot.services.ui_service import UIService
        ui_service = UIService()
        keyboard = ui_service.create_back_keyboard("support")
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        logger.info(f"❓ Показан FAQ для пользователя {callback.from_user.id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_faq: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

async def handle_contact_support(callback: CallbackQuery):
    """
    Обработчик обращения в поддержку
    
    Показывает контакты для связи
    """
    try:
        user_id = callback.from_user.id
        first_name = callback.from_user.first_name or "Пользователь"
        
        message_text = f"""
💬 <b>Связь с поддержкой</b>

<b>Привет, {first_name}!</b>

<b>📞 Быстрая связь:</b>
• 💬 Telegram: @YoVPNSupport
• 📧 Email: support@yovpn.com

<b>📋 При обращении укажите:</b>
• Ваш ID: <code>{user_id}</code>
• Описание проблемы
• Скриншоты (если есть)
• Время возникновения проблемы

<b>⏱️ Время ответа:</b>
• Обычные вопросы: до 2 часов
• Технические проблемы: до 6 часов
• Экстренные случаи: до 30 минут

<b>💡 Советы:</b>
• Опишите проблему подробно
• Приложите скриншоты
• Укажите устройство и ОС
• Сохраните ID для быстрого решения

<b>🆘 Экстренная поддержка:</b>
Если проблема критическая, напишите "СРОЧНО" в начале сообщения.
        """
        
        from bot.services.ui_service import UIService
        ui_service = UIService()
        keyboard = ui_service.create_back_keyboard("support")
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        logger.info(f"💬 Показаны контакты поддержки для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_contact_support: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

def register_support_handler(dp: Dispatcher):
    """
    Регистрация обработчиков поддержки
    
    Args:
        dp: Диспетчер бота
    """
    dp.callback_query.register(handle_support, F.data == "support")
    dp.callback_query.register(handle_faq, F.data == "faq")
    dp.callback_query.register(handle_contact_support, F.data == "contact_support")
    
    logger.info("✅ Обработчики поддержки зарегистрированы")