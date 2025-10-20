"""
Админ панель для управления ботом
Современный интерфейс для администраторов с полным функционалом
"""

import logging
from typing import Optional, Dict, Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from ..services.user_service import UserService
from ..services.marzban_service import MarzbanService
from ..services.ui_service import UIService

logger = logging.getLogger(__name__)

# Состояния для админ панели
class AdminStates(StatesGroup):
    waiting_user_id = State()
    waiting_balance_amount = State()
    waiting_subscription_days = State()
    waiting_broadcast_message = State()

# Роутер для админ команд
admin_router = Router()

class AdminPanel:
    """
    Современная админ панель с полным функционалом управления
    """
    
    def __init__(self, user_service: UserService, marzban_service: MarzbanService, ui_service: UIService):
        self.user_service = user_service
        self.marzban_service = marzban_service
        self.ui_service = ui_service
        self.admin_users = [123456789]  # ID администраторов (замените на свои)
        
    def is_admin(self, user_id: int) -> bool:
        """Проверить, является ли пользователь администратором"""
        return user_id in self.admin_users
    
    async def get_main_menu(self) -> InlineKeyboardMarkup:
        """Главное меню админ панели"""
        keyboard = [
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
            [InlineKeyboardButton(text="💰 Управление балансом", callback_data="admin_balance")],
            [InlineKeyboardButton(text="🔧 Управление подписками", callback_data="admin_subscriptions")],
            [InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="⚙️ Настройки Marzban", callback_data="admin_marzban")],
            [InlineKeyboardButton(text="📈 Аналитика", callback_data="admin_analytics")],
            [InlineKeyboardButton(text="🔒 Безопасность", callback_data="admin_security")],
            [InlineKeyboardButton(text="❌ Закрыть", callback_data="admin_close")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    async def get_stats_menu(self) -> InlineKeyboardMarkup:
        """Меню статистики"""
        keyboard = [
            [InlineKeyboardButton(text="📊 Общая статистика", callback_data="admin_stats_general")],
            [InlineKeyboardButton(text="👥 Статистика пользователей", callback_data="admin_stats_users")],
            [InlineKeyboardButton(text="💰 Финансовая статистика", callback_data="admin_stats_finance")],
            [InlineKeyboardButton(text="🔧 Статистика Marzban", callback_data="admin_stats_marzban")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    async def get_users_menu(self) -> InlineKeyboardMarkup:
        """Меню управления пользователями"""
        keyboard = [
            [InlineKeyboardButton(text="🔍 Найти пользователя", callback_data="admin_find_user")],
            [InlineKeyboardButton(text="📋 Список всех пользователей", callback_data="admin_list_users")],
            [InlineKeyboardButton(text="👥 Активные пользователи", callback_data="admin_active_users")],
            [InlineKeyboardButton(text="💸 Пользователи с балансом", callback_data="admin_users_with_balance")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    async def get_balance_menu(self) -> InlineKeyboardMarkup:
        """Меню управления балансом"""
        keyboard = [
            [InlineKeyboardButton(text="➕ Пополнить баланс", callback_data="admin_add_balance")],
            [InlineKeyboardButton(text="➖ Списать с баланса", callback_data="admin_subtract_balance")],
            [InlineKeyboardButton(text="🔧 Установить баланс", callback_data="admin_set_balance")],
            [InlineKeyboardButton(text="📊 Статистика балансов", callback_data="admin_balance_stats")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    async def get_subscription_menu(self) -> InlineKeyboardMarkup:
        """Меню управления подписками"""
        keyboard = [
            [InlineKeyboardButton(text="✅ Активировать подписку", callback_data="admin_activate_subscription")],
            [InlineKeyboardButton(text="❌ Деактивировать подписку", callback_data="admin_deactivate_subscription")],
            [InlineKeyboardButton(text="⏰ Продлить подписку", callback_data="admin_extend_subscription")],
            [InlineKeyboardButton(text="📊 Статистика подписок", callback_data="admin_subscription_stats")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="admin_back")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    async def get_general_stats(self) -> str:
        """Получить общую статистику"""
        try:
            users = await self.user_service.get_all_users()
            total_users = len(users)
            
            active_subscriptions = sum(1 for user in users.values() if user.get('subscription_active', False))
            total_balance = sum(user.get('balance', 0) for user in users.values())
            total_payments = sum(user.get('total_payments', 0) for user in users.values())
            
            # Статистика Marzban
            marzban_stats = await self.marzban_service.get_system_stats()
            marzban_info = ""
            if marzban_stats:
                marzban_info = f"""
🔧 **Marzban:**
• Статус: {'🟢 Онлайн' if self.marzban_service.is_available() else '🔴 Офлайн'}
• Пользователи: {marzban_stats.get('users', 'N/A')}
• Трафик: {marzban_stats.get('traffic', 'N/A')}
"""
            
            stats_text = f"""
📊 **ОБЩАЯ СТАТИСТИКА**

👥 **Пользователи:**
• Всего: {total_users}
• Активные подписки: {active_subscriptions}
• Процент активности: {(active_subscriptions/total_users*100):.1f}% (если есть пользователи)

💰 **Финансы:**
• Общий баланс: {total_balance:.2f} ₽
• Общие платежи: {total_payments:.2f} ₽
• Средний баланс: {total_balance/total_users:.2f} ₽ (если есть пользователи)

{marzban_info}

🕐 **Время:** {self.ui_service.get_current_time()}
"""
            return stats_text
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики: {e}")
            return f"❌ Ошибка получения статистики: {e}"
    
    async def get_user_stats(self, user_id: int) -> str:
        """Получить статистику конкретного пользователя"""
        try:
            user = await self.user_service.get_user(user_id)
            if not user:
                return f"❌ Пользователь с ID {user_id} не найден"
            
            stats = await self.user_service.get_user_stats(user_id)
            
            stats_text = f"""
👤 **ПОЛЬЗОВАТЕЛЬ #{user_id}**

📝 **Информация:**
• Имя: {user.get('first_name', 'N/A')}
• Username: @{user.get('username', 'N/A')}
• Реферальный код: `{user.get('referral_code', 'N/A')}`

💰 **Финансы:**
• Баланс: {stats.get('balance', 0):.2f} ₽
• Всего платежей: {stats.get('total_payments', 0):.2f} ₽

🔧 **Подписка:**
• Статус: {'✅ Активна' if stats.get('subscription_active') else '❌ Неактивна'}
• Дней: {stats.get('subscription_days', 0)}

📊 **Активность:**
• Рефералов: {stats.get('referrals_count', 0)}
• Создан: {stats.get('created_at', 'N/A')}
• Последняя активность: {stats.get('last_activity', 'N/A')}
"""
            return stats_text
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения статистики пользователя: {e}")
            return f"❌ Ошибка получения статистики пользователя: {e}"
    
    async def get_users_list(self, limit: int = 10) -> str:
        """Получить список пользователей"""
        try:
            users = await self.user_service.get_all_users()
            
            if not users:
                return "📋 Список пользователей пуст"
            
            # Сортируем по дате создания
            sorted_users = sorted(users.values(), 
                                key=lambda x: x.get('created_at', ''), 
                                reverse=True)
            
            users_text = f"📋 **ПОЛЬЗОВАТЕЛИ** (показано {min(limit, len(sorted_users))} из {len(users)})\n\n"
            
            for i, user in enumerate(sorted_users[:limit], 1):
                user_id = user.get('user_id', 'N/A')
                first_name = user.get('first_name', 'N/A')
                username = user.get('username', 'N/A')
                balance = user.get('balance', 0)
                subscription_active = user.get('subscription_active', False)
                
                status_emoji = "✅" if subscription_active else "❌"
                username_text = f"@{username}" if username != 'N/A' else "Без username"
                
                users_text += f"{i}. **{first_name}** ({username_text})\n"
                users_text += f"   ID: `{user_id}` | Баланс: {balance:.2f} ₽ | Подписка: {status_emoji}\n\n"
            
            return users_text
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка пользователей: {e}")
            return f"❌ Ошибка получения списка пользователей: {e}"

# Инициализация админ панели
admin_panel = None

def init_admin_panel(user_service: UserService, marzban_service: MarzbanService, ui_service: UIService):
    """Инициализировать админ панель"""
    global admin_panel
    admin_panel = AdminPanel(user_service, marzban_service, ui_service)

# Обработчики команд
@admin_router.message(Command("admin"))
async def admin_command(message: Message):
    """Команда /admin - открыть админ панель"""
    if not admin_panel or not admin_panel.is_admin(message.from_user.id):
        await message.reply("❌ У вас нет прав администратора")
        return
    
    keyboard = await admin_panel.get_main_menu()
    await message.reply(
        "🔧 **АДМИН ПАНЕЛЬ**\n\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

# Обработчики callback'ов
@admin_router.callback_query(F.data == "admin_stats")
async def admin_stats_callback(callback: CallbackQuery):
    """Обработчик статистики"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    keyboard = await admin_panel.get_stats_menu()
    await callback.message.edit_text(
        "📊 **СТАТИСТИКА**\n\nВыберите тип статистики:",
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_stats_general")
async def admin_stats_general_callback(callback: CallbackQuery):
    """Общая статистика"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    stats_text = await admin_panel.get_general_stats()
    keyboard = await admin_panel.get_stats_menu()
    
    await callback.message.edit_text(
        stats_text,
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_users")
async def admin_users_callback(callback: CallbackQuery):
    """Обработчик пользователей"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    keyboard = await admin_panel.get_users_menu()
    await callback.message.edit_text(
        "👥 **УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ**\n\nВыберите действие:",
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_list_users")
async def admin_list_users_callback(callback: CallbackQuery):
    """Список пользователей"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    users_text = await admin_panel.get_users_list()
    keyboard = await admin_panel.get_users_menu()
    
    await callback.message.edit_text(
        users_text,
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_balance")
async def admin_balance_callback(callback: CallbackQuery):
    """Обработчик баланса"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    keyboard = await admin_panel.get_balance_menu()
    await callback.message.edit_text(
        "💰 **УПРАВЛЕНИЕ БАЛАНСОМ**\n\nВыберите действие:",
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_subscriptions")
async def admin_subscriptions_callback(callback: CallbackQuery):
    """Обработчик подписок"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    keyboard = await admin_panel.get_subscription_menu()
    await callback.message.edit_text(
        "🔧 **УПРАВЛЕНИЕ ПОДПИСКАМИ**\n\nВыберите действие:",
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_back")
async def admin_back_callback(callback: CallbackQuery):
    """Назад в главное меню"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    keyboard = await admin_panel.get_main_menu()
    await callback.message.edit_text(
        "🔧 **АДМИН ПАНЕЛЬ**\n\nВыберите действие:",
        reply_markup=keyboard
    )

@admin_router.callback_query(F.data == "admin_close")
async def admin_close_callback(callback: CallbackQuery):
    """Закрыть админ панель"""
    await callback.message.delete()
    await callback.answer("✅ Админ панель закрыта")

# Обработчики для управления балансом
@admin_router.callback_query(F.data == "admin_add_balance")
async def admin_add_balance_callback(callback: CallbackQuery, state: FSMContext):
    """Добавить баланс"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_user_id)
    await callback.message.edit_text(
        "💰 **ПОПОЛНЕНИЕ БАЛАНСА**\n\n"
        "Введите ID пользователя:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_back")]
        ])
    )

@admin_router.message(StateFilter(AdminStates.waiting_user_id))
async def process_user_id(message: Message, state: FSMContext):
    """Обработка ID пользователя"""
    try:
        user_id = int(message.text)
        await state.update_data(user_id=user_id)
        await state.set_state(AdminStates.waiting_balance_amount)
        
        await message.reply(
            f"✅ ID пользователя: {user_id}\n\n"
            "Введите сумму для пополнения:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_back")]
            ])
        )
    except ValueError:
        await message.reply("❌ Неверный формат ID. Введите число:")

@admin_router.message(StateFilter(AdminStates.waiting_balance_amount))
async def process_balance_amount(message: Message, state: FSMContext):
    """Обработка суммы баланса"""
    try:
        amount = float(message.text)
        data = await state.get_data()
        user_id = data['user_id']
        
        # Обновляем баланс
        success = await admin_panel.user_service.update_user_balance(user_id, amount, "add")
        
        if success:
            user_stats = await admin_panel.get_user_stats(user_id)
            await message.reply(
                f"✅ Баланс пользователя {user_id} пополнен на {amount:.2f} ₽\n\n{user_stats}",
                reply_markup=await admin_panel.get_balance_menu()
            )
        else:
            await message.reply(
                f"❌ Ошибка пополнения баланса для пользователя {user_id}",
                reply_markup=await admin_panel.get_balance_menu()
            )
        
        await state.clear()
        
    except ValueError:
        await message.reply("❌ Неверный формат суммы. Введите число:")

# Обработчики для управления подписками
@admin_router.callback_query(F.data == "admin_activate_subscription")
async def admin_activate_subscription_callback(callback: CallbackQuery, state: FSMContext):
    """Активировать подписку"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_user_id)
    await callback.message.edit_text(
        "✅ **АКТИВАЦИЯ ПОДПИСКИ**\n\n"
        "Введите ID пользователя:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_back")]
        ])
    )

@admin_router.callback_query(F.data == "admin_find_user")
async def admin_find_user_callback(callback: CallbackQuery, state: FSMContext):
    """Найти пользователя"""
    if not admin_panel or not admin_panel.is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав", show_alert=True)
        return
    
    await state.set_state(AdminStates.waiting_user_id)
    await callback.message.edit_text(
        "🔍 **ПОИСК ПОЛЬЗОВАТЕЛЯ**\n\n"
        "Введите ID пользователя:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="admin_back")]
        ])
    )

@admin_router.message(StateFilter(AdminStates.waiting_user_id))
async def process_find_user(message: Message, state: FSMContext):
    """Обработка поиска пользователя"""
    try:
        user_id = int(message.text)
        user_stats = await admin_panel.get_user_stats(user_id)
        
        await message.reply(
            user_stats,
            reply_markup=await admin_panel.get_users_menu()
        )
        await state.clear()
        
    except ValueError:
        await message.reply("❌ Неверный формат ID. Введите число:")