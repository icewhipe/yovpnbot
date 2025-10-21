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

async def handle_support(callback: CallbackQuery, **kwargs):
    """
    Обработчик кнопки "Поддержка"
    
    Показывает меню поддержки и FAQ
    Отправляет уведомление администратору при обращении пользователя
    """
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Пользователь"
    username = callback.from_user.username or "нет username"
    
    try:
        message_text = f"""
🆘 <b>Поддержка YoVPN</b>

<blockquote>Мы всегда готовы помочь вам с любыми вопросами!</blockquote>

📞 <b>Способы связи:</b>
├ 💬 <b>Telegram:</b> @YoVPNSupport
├ 📧 <b>Email:</b> support@yovpn.com
└ 🌐 <b>Сайт:</b> https://yovpn.com/support

⏰ <b>Время работы поддержки:</b>
├ <i>Пн-Пт:</i> <code>09:00 - 21:00</code>
├ <i>Сб-Вс:</i> <code>10:00 - 18:00</code>
└ <i>Экстренная поддержка:</i> <code>24/7</code>

🔍 <b>Популярные вопросы:</b>
• Как настроить VPN на моём устройстве?
• Как пополнить баланс?
• Почему не работает подключение?
• Как отменить или приостановить подписку?

📋 <b>При обращении укажите:</b>
├ <b>Ваш ID:</b> <code>{user_id}</code>
├ <b>Описание проблемы</b>
├ <b>Скриншоты</b> (если возможно)
└ <b>Время возникновения</b>

<i>💡 Совет: Сначала проверьте раздел FAQ - возможно, ваш вопрос уже решён!</i>
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
    
    Показывает часто задаваемые вопросы с современным форматированием
    """
    try:
        message_text = f"""
❓ <b>Часто задаваемые вопросы (FAQ)</b>

<blockquote>Здесь собраны ответы на самые популярные вопросы наших пользователей</blockquote>

🔧 <b>НАСТРОЙКА VPN</b>

<b>Q:</b> <i>Как настроить VPN на телефоне Android?</i>
<b>A:</b> 
├ 1. Скачайте <b>V2rayNG</b> из Google Play
├ 2. Скопируйте конфигурацию из бота
├ 3. В приложении нажмите <code>+</code> → <code>Импорт из буфера</code>
└ 4. Нажмите <code>Подключиться</code> ✅

<b>Q:</b> <i>Как настроить VPN на iPhone/iPad?</i>
<b>A:</b> 
├ 1. Скачайте <b>Streisand</b> из App Store
├ 2. Скопируйте конфигурацию из бота
├ 3. Откройте приложение и вставьте конфигурацию
└ 4. Нажмите <code>Подключиться</code> ✅

<b>Q:</b> <i>Как настроить VPN на компьютере?</i>
<b>A:</b>
<b>Windows:</b> Скачайте V2rayN → Импортируйте конфигурацию → Подключитесь
<b>macOS:</b> Скачайте V2rayU → Импортируйте конфигурацию → Подключитесь
<b>Linux:</b> Установите v2ray-core → Создайте config.json → Запустите службу

━━━━━━━━━━━━━━━━━━

💰 <b>ПЛАТЕЖИ И БАЛАНС</b>

<b>Q:</b> <i>Как пополнить баланс?</i>
<b>A:</b> Нажмите <code>💳 Пополнить</code> в главном меню → Выберите сумму → Выберите способ оплаты

<b>Q:</b> <i>Сколько стоит подписка?</i>
<b>A:</b> <b>4 рубля в день</b> 💰
Списание происходит автоматически каждый день в <code>00:00 МСК</code>

<b>Q:</b> <i>Что будет, если закончатся деньги на балансе?</i>
<b>A:</b> Подписка приостановится автоматически ⏸️
После пополнения баланса она возобновится сразу же! 🔄

━━━━━━━━━━━━━━━━━━

🔒 <b>БЕЗОПАСНОСТЬ</b>

<b>Q:</b> <i>Безопасен ли ваш VPN?</i>
<b>A:</b> <b>Да!</b> ✅
├ 🔐 Современное шифрование <code>AES-256</code>
├ 🚫 Без логов активности (<code>No-logs policy</code>)
└ 🛡️ Защита от утечек DNS

<b>Q:</b> <i>Можно ли использовать на нескольких устройствах?</i>
<b>A:</b> <b>Да!</b> Одну подписку можно использовать на <b>неограниченном</b> количестве устройств 📱💻

━━━━━━━━━━━━━━━━━━

🔄 <b>ТЕХНИЧЕСКИЕ ВОПРОСЫ</b>

<b>Q:</b> <i>Почему не работает подключение?</i>
<b>A:</b> Проверьте:
├ 1. Интернет-соединение 📶
├ 2. Правильность конфигурации ⚙️
├ 3. Актуальность приложения 🔄
└ 4. Достаточный баланс 💰

<b>Q:</b> <i>Как отменить подписку?</i>
<b>A:</b> Просто не пополняйте баланс. Подписка автоматически приостановится при <code>0 ₽</code>

<i>💡 Не нашли ответ? Обратитесь в поддержку!</i>
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

async def handle_contact_support(callback: CallbackQuery, **kwargs):
    """
    Обработчик обращения в поддержку
    
    Показывает контакты для связи и отправляет уведомление админу
    """
    try:
        user_id = callback.from_user.id
        first_name = callback.from_user.first_name or "Пользователь"
        username = callback.from_user.username
        
        # Получаем сервисы из middleware
        services = kwargs.get("services")
        
        # Отправляем уведомление администратору
        ADMIN_ID = 7610842643
        try:
            if services:
                notification_service = services.get_notification_service()
                await notification_service.send_notification(
                    ADMIN_ID,
                    f"🆘 <b>Обращение в поддержку</b>\n\n"
                    f"👤 <b>Пользователь:</b> {first_name}\n"
                    f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
                    f"📱 <b>Username:</b> @{username if username else 'нет'}\n"
                    f"⏰ <b>Время:</b> {services.get_ui_service().get_current_time()}"
                )
        except Exception as e:
            logger.warning(f"⚠️ Не удалось отправить уведомление админу: {e}")
        
        message_text = f"""
💬 <b>Связь с поддержкой</b>

<blockquote>Привет, {first_name}! Мы готовы помочь вам 24/7 🌟</blockquote>

📞 <b>Быстрая связь:</b>
├ 💬 <b>Telegram:</b> @YoVPNSupport
└ 📧 <b>Email:</b> support@yovpn.com

📋 <b>При обращении обязательно укажите:</b>
├ 🆔 <b>Ваш ID:</b> <code>{user_id}</code>
├ 📝 <b>Описание проблемы</b> (подробно)
├ 📸 <b>Скриншоты</b> (если возможно)
└ ⏰ <b>Время возникновения</b>

⏱️ <b>Среднее время ответа:</b>
├ ✉️ <i>Обычные вопросы:</i> <code>до 2 часов</code>
├ 🔧 <i>Технические проблемы:</i> <code>до 6 часов</code>
└ 🚨 <i>Экстренные случаи:</i> <code>до 30 минут</code>

💡 <b>Советы для быстрого решения:</b>
• Опишите проблему максимально подробно
• Приложите скриншоты ошибок
• Укажите модель устройства и версию ОС
• Сохраните ваш ID: <code>{user_id}</code>

🆘 <b>Экстренная поддержка:</b>
<blockquote expandable>Если проблема <b>критическая</b> (полное отсутствие доступа, проблемы с платежом и т.д.), 
напишите слово <code>СРОЧНО</code> в начале вашего сообщения, и мы ответим в приоритетном порядке!</blockquote>

<i>✅ Ваше обращение зарегистрировано, администратор уведомлён!</i>
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

async def handle_support_message(message: Message, **kwargs):
    """
    Обработчик текстовых сообщений в поддержку
    
    Пересылает сообщение администратору
    """
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username
    
    # Получаем сервисы
    services = kwargs.get("services")
    ADMIN_ID = 7610842643
    
    try:
        # Отправляем сообщение администратору
        if services:
            notification_service = services.get_notification_service()
            await notification_service.send_notification(
                ADMIN_ID,
                f"💬 <b>Сообщение в поддержку</b>\n\n"
                f"👤 <b>От:</b> {first_name} (@{username if username else 'нет'})\n"
                f"🆔 <b>ID:</b> <code>{user_id}</code>\n\n"
                f"<blockquote>{message.text}</blockquote>\n\n"
                f"⏰ <b>Время:</b> {services.get_ui_service().get_current_time()}"
            )
            
            await message.reply(
                f"✅ <b>Ваше сообщение отправлено в поддержку!</b>\n\n"
                f"Администратор получит ваше обращение и свяжется с вами в ближайшее время.\n\n"
                f"<i>Среднее время ответа: 2-6 часов</i>"
            )
            logger.info(f"📨 Сообщение от пользователя {user_id} переслано администратору")
        else:
            await message.reply("❌ Сервис временно недоступен. Попробуйте позже.")
            
    except Exception as e:
        logger.error(f"❌ Ошибка пересылки сообщения в поддержку: {e}")
        await message.reply("❌ Ошибка отправки сообщения. Попробуйте позже.")

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