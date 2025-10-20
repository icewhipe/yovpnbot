"""
Обработчик команды /start
Приветствие пользователей и главное меню
"""

import logging
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from assets.emojis.interface import EMOJI, get_emoji_combination

logger = logging.getLogger(__name__)

async def start_command(message: Message):
    """
    Обработчик команды /start
    
    Отправляет приветственное сообщение с анимированным эффектом
    и показывает главное меню бота
    
    Args:
        message: Сообщение от пользователя
    """
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username
    
    logger.info(f"👋 Новый пользователь: ID={user_id}, Username=@{username}, Name={first_name}")
    
    # Получаем сервисы из контекста
    services = message.bot.get("services")
    if not services:
        logger.error("❌ Сервисы не найдены в контексте бота")
        await message.reply("❌ Ошибка инициализации. Попробуйте позже.")
        return
    
    try:
        # Отправляем приветственное сообщение с эффектом
        await services.get_animation_service().send_welcome_message(message, first_name)
        
        # Создаем или обновляем запись пользователя
        user_service = services.get_user_service()
        user = await user_service.create_or_update_user(
            user_id=user_id,
            username=username,
            first_name=first_name
        )
        
        logger.info(f"✅ Пользователь {first_name} успешно зарегистрирован")
        
    except Exception as e:
        logger.error(f"❌ Ошибка в команде /start: {e}")
        await message.reply(
            f"❌ Произошла ошибка при регистрации. "
            f"Попробуйте позже или обратитесь в поддержку."
        )

def register_start_handler(dp: Dispatcher):
    """
    Регистрация обработчика команды /start
    
    Args:
        dp: Диспетчер бота
    """
    dp.message.register(start_command, CommandStart())
    logger.info("✅ Обработчик команды /start зарегистрирован")