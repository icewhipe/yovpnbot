"""
Обработчик команды /start
Приветствие пользователей и главное меню
"""

import asyncio
import logging
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from assets.emojis.interface import EMOJI, get_emoji_combination

logger = logging.getLogger(__name__)

async def start_command(message: Message, **kwargs):
    """
    Обработчик команды /start
    
    Отправляет приветственное сообщение с анимированным эффектом
    и показывает главное меню бота. Для новых пользователей показывает
    onboarding-анимацию и начисляет бонус 15₽.
    
    Args:
        message: Сообщение от пользователя
        **kwargs: Дополнительные данные, включая services из middleware
    """
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username
    
    logger.info(f"👋 Пользователь: ID={user_id}, Username=@{username}, Name={first_name}")
    
    # Получаем сервисы из middleware
    services = kwargs.get("services")
    if not services:
        logger.error("❌ Сервисы не найдены в middleware")
        await message.reply("❌ Ошибка инициализации. Попробуйте позже.")
        return
    
    try:
        user_service = services.get_user_service()
        animation_service = services.get_animation_service()
        
        # Проверяем, является ли пользователь новым
        existing_user = await user_service.get_user(user_id)
        is_new_user = existing_user is None
        
        if is_new_user:
            logger.info(f"🎉 Новый пользователь: {first_name} (ID: {user_id})")
            
            # Показываем onboarding-анимацию для нового пользователя
            await show_onboarding_animation(message, first_name, animation_service)
            
            # Создаем пользователя (с автоматическим бонусом 15₽)
            user = await user_service.create_or_update_user(
                user_id=user_id,
                username=username,
                first_name=first_name
            )
            
            logger.info(f"✅ Пользователь {first_name} зарегистрирован с бонусом 15₽")
        else:
            logger.info(f"👋 Возвращение пользователя: {first_name} (ID: {user_id})")
            
            # Обновляем данные существующего пользователя
            user = await user_service.create_or_update_user(
                user_id=user_id,
                username=username,
                first_name=first_name
            )
            
            # Отправляем обычное приветственное сообщение
            await animation_service.send_welcome_message(message, first_name)
        
    except Exception as e:
        logger.error(f"❌ Ошибка в команде /start: {e}")
        await message.reply(
            f"❌ Произошла ошибка при регистрации. "
            f"Попробуйте позже или обратитесь в поддержку."
        )

async def show_onboarding_animation(message: Message, first_name: str, animation_service):
    """
    Показать onboarding-анимацию для нового пользователя
    
    Последовательность:
    1. "🔄 Настраиваем подключение к VPN-серверу..."
    2. "🔐 Генерируем ключ шифрования..."
    3. "🌐 Подключаем к защищённой сети..."
    4. "🎁 Дарим тебе стартовый баланс: +15₽"
    5. Приветственное сообщение с главным меню
    
    Args:
        message: Сообщение пользователя
        first_name: Имя пользователя
        animation_service: Сервис анимаций
    """
    try:
        # Шаг 1: Настройка подключения
        step_msg = await message.answer(
            "🔄 <b>Настраиваем подключение к VPN-серверу...</b>",
            parse_mode='HTML'
        )
        await asyncio.sleep(1.5)
        
        # Шаг 2: Генерация ключа
        await step_msg.edit_text(
            "🔐 <b>Генерируем ключ шифрования...</b>",
            parse_mode='HTML'
        )
        await asyncio.sleep(1.5)
        
        # Шаг 3: Подключение к сети
        await step_msg.edit_text(
            "🌐 <b>Подключаем к защищённой сети...</b>",
            parse_mode='HTML'
        )
        await asyncio.sleep(1.5)
        
        # Шаг 4: Бонус
        await step_msg.edit_text(
            f"🎁 <b>Дарим тебе стартовый баланс: +15₽</b>\n\n"
            f"✨ Это <b>3 дня</b> бесплатного VPN!",
            parse_mode='HTML'
        )
        await asyncio.sleep(2.0)
        
        # Удаляем анимационное сообщение
        await step_msg.delete()
        
        # Шаг 5: Показываем приветственное сообщение с меню
        await animation_service.send_welcome_message(message, first_name)
        
        logger.info(f"✅ Onboarding завершен для пользователя {first_name}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в onboarding анимации: {e}")
        # Fallback: показываем обычное приветствие
        await animation_service.send_welcome_message(message, first_name)

def register_start_handler(dp: Dispatcher):
    """
    Регистрация обработчика команды /start
    
    Args:
        dp: Диспетчер бота
    """
    dp.message.register(start_command, CommandStart())
    logger.info("✅ Обработчик команды /start зарегистрирован")