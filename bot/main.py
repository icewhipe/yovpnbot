#!/usr/bin/env python3
"""
YoVPN Telegram Bot - Главный файл
Современный бот для продажи VPN-подписок с ежедневной оплатой

Особенности:
- Анимированные эффекты сообщений
- Современный UX/UI дизайн
- Ежедневная модель оплаты (4 рубля в день)
- Полная безопасность и валидация
- Асинхронная архитектура
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Добавляем корневую папку в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Импорты конфигурации и сервисов
from src.config import config
from bot.handlers import register_handlers, init_admin_panel
from bot.middleware import register_middleware
from bot.services import BotServices

# Настройка логирования
logging.basicConfig(
   log_to_file = os.getenv('LOG_TO_FILE', '0') == '1'
log_file = os.getenv('LOG_FILE', '/tmp/bot.log')

handlers = [logging.StreamHandler(sys.stdout)]
if log_to_file:
    handlers = [logging.FileHandler(log_file)]

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO').upper(),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers,
)
logger = logging.getLogger(__name__)

class YoVPNBot:
    """
    Главный класс бота YoVPN
    
    Отвечает за:
    - Инициализацию бота и диспетчера
    - Регистрацию обработчиков и middleware
    - Запуск и остановку бота
    - Управление сервисами
    """
    
    def __init__(self):
        """Инициализация бота"""
        self.bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher(storage=MemoryStorage())
        
        # Создаем сервисы ОДИН РАЗ
        self.services = BotServices(self.bot)
        
        # Регистрируем middleware с готовыми сервисами
        register_middleware(self.dp, self.services)
        
        # Регистрируем обработчики
        register_handlers(self.dp)
        
        # Инициализируем админ панель с ВСЕМИ сервисами
        init_admin_panel(
            self.services.user_service,
            self.services.marzban_service,
            self.services.ui_service,
            self.services.animation_service  # ИСПРАВЛЕНО: добавлен animation_service
        )
        
        logger.info("YoVPN Bot инициализирован")
    
    async def start(self):
        """Запуск бота"""
        try:
            logger.info("🚀 Запуск YoVPN Bot...")
            
            # Запускаем фоновые задачи
            await self.services.start_background_tasks()
            
            # Запускаем бота
            await self.dp.start_polling(
                self.bot,
                allowed_updates=["message", "callback_query"]
            )
            
        except Exception as e:
            logger.error(f"❌ Ошибка при запуске бота: {e}")
            raise
    
    async def stop(self):
        """Остановка бота"""
        try:
            logger.info("🛑 Остановка YoVPN Bot...")
            
            # Останавливаем фоновые задачи
            await self.services.stop_background_tasks()
            
            # Закрываем сессию бота
            await self.bot.session.close()
            
            logger.info("✅ Бот успешно остановлен")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при остановке бота: {e}")

async def main():
    """Главная функция"""
    bot = YoVPNBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 До свидания!")
    except Exception as e:
        logger.error(f"💥 Фатальная ошибка: {e}")
        sys.exit(1)
