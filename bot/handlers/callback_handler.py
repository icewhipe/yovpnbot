"""
Обработчик callback запросов
Центральный обработчик для всех callback запросов
"""

import logging
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram import F

from assets.emojis.interface import EMOJI

logger = logging.getLogger(__name__)

async def handle_main_menu(callback: CallbackQuery, **kwargs):
    """
    Обработчик возврата в главное меню
    
    Показывает главное меню бота
    """
    user_id = callback.from_user.id
    first_name = callback.from_user.first_name or "Пользователь"
    
    try:
        # Получаем сервисы из middleware
        services = kwargs.get("services")
        if not services:
            await callback.answer("❌ Сервисы недоступны", show_alert=True)
            return
        
        user_service = services.get_user_service()
        ui_service = services.get_ui_service()
        
        # Получаем данные пользователя
        user = await user_service.get_or_create_user(
            user_id=user_id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name or "Пользователь"
        )
        
        # Получаем статистику
        stats = await user_service.get_user_stats(user_id)
        balance = stats.get('balance', 0.0)
        subscription_active = stats.get('subscription_active', False)
        subscription_days = stats.get('subscription_days', 0)
        
        # Форматируем приветственное сообщение
        message_text = f"""
🏠 <b>Главное меню</b>

👋 <b>Привет, {first_name}!</b>

💰 <b>Баланс:</b> {balance:.2f} ₽
📅 <b>Дней доступа:</b> {subscription_days} дней
📊 <b>Подписка:</b> {'Активна' if subscription_active else 'Неактивна'}

<b>Выберите действие:</b>
        """
        
        # Создаем клавиатуру главного меню
        keyboard = ui_service.create_main_menu_keyboard()
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        logger.info(f"🏠 Показано главное меню для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_main_menu: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

async def handle_stats(callback: CallbackQuery, **kwargs):
    """
    Обработчик кнопки "Статистика"
    
    Показывает статистику пользователя
    """
    user_id = callback.from_user.id
    
    try:
        # Получаем сервисы из middleware
        services = kwargs.get("services")
        if not services:
            await callback.answer("❌ Сервисы недоступны", show_alert=True)
            return
        
        user_service = services.get_user_service()
        ui_service = services.get_ui_service()
        
        # Получаем данные пользователя
        user = await user_service.get_or_create_user(
            user_id=user_id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name or "Пользователь"
        )
        
        # Получаем статистику
        stats = await user_service.get_user_stats(user_id)
        balance = stats.get('balance', 0.0)
        total_payments = stats.get('total_payments', 0.0)
        referrals_count = stats.get('referrals_count', 0)
        created_at = stats.get('created_at', 'Неизвестно')
        
        message_text = f"""
📊 <b>Ваша статистика</b>

<b>💰 Финансы:</b>
• Текущий баланс: {balance:.2f} ₽
• Всего пополнено: {total_payments:.2f} ₽
• Дней доступа: {int(balance / 4)} дней

<b>👥 Рефералы:</b>
• Приглашено: {referrals_count} человек
• Заработано: {referrals_count * 20} ₽
• Реферальный код: <code>ref_{user_id}</code>

<b>📅 Аккаунт:</b>
• Дата регистрации: {created_at[:10] if created_at != 'Неизвестно' else 'Неизвестно'}
• Статус: Активен
• Уведомления: Включены

<b>🎯 Достижения:</b>
• {'🥇 Первый платеж' if total_payments > 0 else '🥉 Новый пользователь'}
• {'🥈 Постоянный клиент' if total_payments > 100 else ''}
• {'🥉 Мастер рефералов' if referrals_count > 5 else ''}
        """
        
        keyboard = ui_service.create_back_keyboard("main_menu")
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        logger.info(f"📊 Показана статистика пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_stats: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

async def handle_referrals(callback: CallbackQuery, **kwargs):
    """
    Обработчик кнопки "Рефералы"
    
    Показывает информацию о реферальной программе
    """
    user_id = callback.from_user.id
    
    try:
        # Получаем сервисы из middleware
        services = kwargs.get("services")
        if not services:
            await callback.answer("❌ Сервисы недоступны", show_alert=True)
            return
        
        user_service = services.get_user_service()
        ui_service = services.get_ui_service()
        
        # Получаем данные пользователя
        user = await user_service.get_or_create_user(
            user_id=user_id,
            username=callback.from_user.username,
            first_name=callback.from_user.first_name or "Пользователь"
        )
        
        # Получаем статистику рефералов
        stats = await user_service.get_user_stats(user_id)
        referrals_count = stats.get('referrals_count', 0)
        referral_code = user.get('referral_code', f"ref_{user_id}")
        
        # Создаем реферальную ссылку
        bot_username = callback.bot.get_me().username
        referral_link = f"https://t.me/{bot_username}?start={referral_code}"
        
        message_text = f"""
🎁 <b>Реферальная программа</b>

<b>💰 Зарабатывайте с друзьями!</b>

<b>📊 Ваша статистика:</b>
• Приглашено: {referrals_count} человек
• Заработано: {referrals_count * 20} ₽
• Реферальный код: <code>{referral_code}</code>

<b>🔗 Ваша реферальная ссылка:</b>
<code>{referral_link}</code>

<b>💡 Как это работает:</b>
1. Поделитесь ссылкой с друзьями
2. Друг регистрируется по вашей ссылке
3. Вы получаете 20 ₽ на баланс
4. Друг получает 20 ₽ бонус

<b>📋 Правила:</b>
• Бонус начисляется после первой оплаты друга
• Максимум 100 рефералов в месяц
• Бонусы начисляются автоматически
• Запрещено создание фейковых аккаунтов
        """
        
        keyboard = ui_service.create_back_keyboard("main_menu")
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        logger.info(f"🎁 Показана реферальная программа для пользователя {user_id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_referrals: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

async def handle_instructions(callback: CallbackQuery):
    """
    Обработчик кнопки "Инструкция"
    
    Показывает подробную инструкцию по настройке VPN
    """
    try:
        message_text = f"""
📋 <b>Подробная инструкция по настройке VPN</b>

<b>📱 Мобильные устройства:</b>

<b>Android:</b>
1. Скачайте приложение V2rayNG из Google Play
2. Откройте приложение
3. Нажмите "+" для добавления сервера
4. Выберите "Из буфера обмена"
5. Вставьте ссылку из бота
6. Нажмите "Подключиться"

<b>iOS:</b>
1. Скачайте приложение OneClick из App Store
2. Откройте приложение
3. Нажмите "Добавить сервер"
4. Вставьте ссылку из бота
5. Нажмите "Подключиться"

<b>💻 Компьютеры:</b>

<b>Windows:</b>
1. Скачайте V2rayN с GitHub
2. Распакуйте архив
3. Запустите v2rayN.exe
4. Нажмите "Серверы" → "Импорт из буфера обмена"
5. Вставьте ссылку из бота
6. Выберите сервер и подключитесь

<b>macOS:</b>
1. Скачайте V2rayU с GitHub
2. Установите приложение
3. Откройте V2rayU
4. Нажмите "Добавить" → "Из буфера обмена"
5. Вставьте ссылку из бота
6. Подключитесь к серверу

<b>🐧 Linux:</b>
1. Установите v2ray-core
2. Создайте конфигурационный файл
3. Вставьте ссылку из бота
4. Запустите v2ray

<b>❓ Нужна помощь?</b>
Обратитесь в поддержку: @YoVPNSupport
        """
        
        from bot.services.ui_service import UIService
        ui_service = UIService()
        keyboard = ui_service.create_back_keyboard("my_subscriptions")
        
        await callback.message.edit_text(
            message_text,
            reply_markup=keyboard
        )
        
        await callback.answer()
        logger.info(f"📋 Показана инструкция для пользователя {callback.from_user.id}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в handle_instructions: {e}")
        await callback.answer("❌ Произошла ошибка", show_alert=True)

def register_callback_handler(dp: Dispatcher):
    """
    Регистрация обработчиков callback запросов
    
    Args:
        dp: Диспетчер бота
    """
    dp.callback_query.register(handle_main_menu, F.data == "main_menu")
    dp.callback_query.register(handle_stats, F.data == "stats")
    dp.callback_query.register(handle_referrals, F.data == "referrals")
    dp.callback_query.register(handle_instructions, F.data == "instructions")
    
    logger.info("✅ Обработчики callback запросов зарегистрированы")