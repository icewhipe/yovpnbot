#!/usr/bin/env python3
"""
Улучшенный Telegram Bot для пользователей Marzban
"""

import os
import sys
import logging
import time
from io import BytesIO

# Добавляем путь к src в sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import telebot
from telebot import types

# Импорты из нашего пакета
from src.config import config
from src.services.user_service import UserService
from src.services.marzban_service import MarzbanService
from src.models.user import User

# Опциональная поддержка генерации QR-кодов
try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание сервисов
user_service = UserService()
marzban_service = MarzbanService()

# Создание бота
bot = telebot.TeleBot(config.BOT_TOKEN)

# Список пользователей, которые уже получили тестовый период
test_users = set()

# Эмодзи для интерфейса
EMOJI = {
    'user': '👤',
    'subscription': '📱',
    'balance': '💰',
    'referral': '👥',
    'info': 'ℹ️',
    'add': '➕',
    'back': '⬅️',
    'home': '🏠',
    'check': '✅',
    'cross': '❌',
    'warning': '⚠️',
    'lock': '🔒',
    'unlock': '🔓',
    'settings': '⚙️',
    'support': '🆘',
    'channel': '📢',
    'link': '🔗',
    'qr': '📱',
    'share': '📤',
    'history': '📊',
    'coupon': '🎫',
    'payment': '💳',
    'device': '📱',
    'wifi': '📶',
    'vpn': '🔒',
    'speed': '⚡',
    'security': '🛡️',
    'no_logs': '🔒',
    'active': '🟢',
    'expired': '🔴',
    'limited': '🟡',
    'on_hold': '🟠',
    'robot': '🤖',
    'rocket': '🚀',
    'gift': '🎁',
    'hourglass': '⏳',
    'loading': '⏳'
}

def handle_error(func):
    """Декоратор для обработки ошибок"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка в функции {func.__name__}: {e}")
            # Здесь можно добавить отправку уведомления администратору
            return None
    return wrapper

@bot.message_handler(commands=['start'])
@handle_error
def start_command(message):
    """Обработчик команды /start: приветствие, бонус, рефералка, начало настройки."""
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username
    
    logger.info(f"Команда /start: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Создаем или получаем запись пользователя
    user = user_service.ensure_user_record(user_id, username, first_name)
    
    # Обрабатываем реферальный параметр: /start ref_<id|username>
    try:
        param = None
        if message.text and ' ' in message.text:
            param = message.text.split(' ', 1)[1].strip()
        if param and param.startswith('ref_'):
            ref_key = param.replace('ref_', '', 1)
            referrer_id = int(ref_key) if ref_key.isdigit() else user_service.find_user_id_by_username(ref_key)
            if referrer_id:
                user_service.record_referral(referrer_id, user_id)
    except Exception as e:
        logger.warning(f"Не удалось обработать реферальный параметр: {e}")
    
    # Приветственный бонус 20 ₽ (однократно)
    if not user.bonus_given:
        user_service.credit_balance(user_id, 20, reason='welcome_bonus')
        user_service.update_user_record(user_id, {"bonus_given": True})
    
    # Если это самый первый /start — показываем приветствие с кнопкой настройки
    if not user.first_start_completed:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['settings']} Настроить VPN", callback_data='start_setup'))
        welcome_text = (
            f"{EMOJI['user']} <b>Добро пожаловать, {first_name}!</b>\n\n"
            f"Вы попали в бота <b>YoVPN</b>. Мы начислили вам <b>20 ₽</b> — это <b>5 дней</b> доступа (4 ₽ = 1 день).\n\n"
            f"<b>Почему YoVPN:</b>\n"
            f"• {EMOJI['speed']} Высокая скорость\n"
            f"• {EMOJI['security']} Надежная защита\n"
            f"• {EMOJI['no_logs']} Без логов\n"
            f"• {EMOJI['active']} Стабильно 24/7\n\n"
            f"Нажмите «Настроить VPN», чтобы начать."
        )
        bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=keyboard)
        user_service.update_user_record(user_id, {"first_start_completed": True})
        return
    
    # Иначе показываем главное меню
    show_main_menu(message)

@bot.callback_query_handler(func=lambda call: True)
@handle_error
def handle_callback(call):
    """Обработчик всех callback запросов"""
    # Создаем объект message с правильными данными пользователя
    class FakeMessage:
        def __init__(self, call):
            self.chat = call.message.chat
            self.message_id = call.message.message_id
            self.from_user = call.from_user
    
    fake_message = FakeMessage(call)
    
    # Маршрутизация callback'ов
    callback_handlers = {
        "add_subscription": show_subscription_options,
        "my_subscriptions": show_my_subscriptions,
        "balance": show_balance_menu,
        "invite_friend": show_invite_menu,
        "my_referrals": show_referrals_menu,
        "about_service": show_about_service,
        "back_to_main": show_main_menu,
        "top_up_balance": show_payment_options,
        "payment_history": show_payment_history,
        "activate_coupon": activate_coupon,
        "share_link": share_referral_link,
        "show_qr": show_qr_code,
        "support_chat": show_support_chat,
        "channel_link": show_channel_link,
        'start_setup': show_setup_step1,
        'continue_setup': continue_setup_flow,
        'back_to_setup_1': show_setup_step1,
        'finish_setup': finish_setup,
        'show_qr_key': show_qr_key,
    }
    
    # Обработка callback'ов с параметрами
    if call.data.startswith("get_test_"):
        username = call.data.replace("get_test_", "")
        get_test_period(fake_message, username)
    elif call.data.startswith("subscribe_"):
        handle_subscription_purchase(fake_message, call.data)
    elif call.data.startswith('choose_device_'):
        device_key = call.data.replace('choose_device_', '')
        show_setup_step2(fake_message, device_key)
    elif call.data.startswith("get_link_"):
        username = call.data.replace("get_link_", "")
        show_vpn_links(fake_message, username)
    elif call.data.startswith("show_vless_"):
        username = call.data.replace("show_vless_", "")
        show_vless_links(fake_message, username)
    elif call.data.startswith("show_sub_"):
        username = call.data.replace("show_sub_", "")
        show_subscription_link(fake_message, username)
    elif call.data.startswith("copy_link_"):
        copy_vless_link(fake_message, call.data)
    elif call.data.startswith("get_configs_"):
        username = call.data.replace("get_configs_", "")
        get_vless_configs(fake_message, username)
    else:
        # Обработка простых callback'ов
        handler = callback_handlers.get(call.data)
        if handler:
            handler(fake_message)
    
    # Отвечаем на callback query
    try:
        bot.answer_callback_query(call.id)
    except Exception as e:
        logger.warning(f"Ошибка ответа на callback query: {e}")

@handle_error
def show_main_menu(message):
    """Показать главное меню"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "Пользователь"
    
    # Если username None, используем first_name
    if not username:
        username = first_name.lower().replace(" ", "_")
    
    logger.info(f"Главное меню: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Проверяем, есть ли у пользователя подписка
    user_info = marzban_service.get_user_info(username) if username else None
    is_new_user = user_id not in test_users
    
    # Получаем статистику пользователя
    user_stats = user_service.get_user_stats(user_id)
    
    # Создаем клавиатуру главного меню
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    if user_info:
        # Пользователь с подпиской
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['add']} Продлить подписку", callback_data="add_subscription"),
            types.InlineKeyboardButton(f"{EMOJI['subscription']} Мои подписки", callback_data="my_subscriptions")
        )
    elif is_new_user:
        # Новый пользователь
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['gift']} Получить тестовый период", callback_data=f"get_test_{username}"),
            types.InlineKeyboardButton(f"{EMOJI['subscription']} Мои подписки", callback_data="my_subscriptions")
        )
    else:
        # Пользователь уже получал тест
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['add']} Купить подписку", callback_data="add_subscription"),
            types.InlineKeyboardButton(f"{EMOJI['subscription']} Мои подписки", callback_data="my_subscriptions")
        )
    
    # Вторая строка: Баланс (длинная кнопка)
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['balance']} Баланс", callback_data="balance")
    )
    
    # Третья строка: Пригласить друга и Мои рефералы
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['referral']} Пригласить друга", callback_data="invite_friend"),
        types.InlineKeyboardButton(f"{EMOJI['referral']} Мои рефералы", callback_data="my_referrals")
    )
    
    # Четвертая строка: О сервисе (длинная кнопка)
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['info']} О сервисе", callback_data="about_service")
    )
    
    # Формируем текст приветствия
    balance = user_stats.get('balance_rub', 0)
    days = user_stats.get('days_remaining', 0)
    
    if user_info:
        # Пользователь с подпиской
        welcome_text = f"""
{EMOJI['user']} <b>Добро пожаловать, {first_name}!</b>

<b>Ваш профиль:</b>
├ ID: {user_id}
├ Username: @{username}
├ Баланс: {balance} ₽ (≈ {days} дн.)
└ Подписок: 1

{EMOJI['rocket']} <b>Выберите действие:</b>
"""
    elif is_new_user:
        # Новый пользователь
        welcome_text = f"""
{EMOJI['user']} <b>Добро пожаловать, {first_name}!</b>

{EMOJI['gift']} <b>Подарок для новых пользователей!</b>
Вы получили 7 дней бесплатного доступа к VPN

<b>Ваш профиль:</b>
├ ID: {user_id}
├ Username: @{username}
├ Баланс: {balance} ₽ (≈ {days} дн.)
└ Подписок: 0

{EMOJI['rocket']} <b>Выберите действие:</b>
"""
    else:
        # Пользователь уже получал тест
        welcome_text = f"""
{EMOJI['user']} <b>Добро пожаловать, {first_name}!</b>

<b>Ваш профиль:</b>
├ ID: {user_id}
├ Username: @{username}
├ Баланс: {balance} ₽ (≈ {days} дн.)
└ Подписок: 0

{EMOJI['rocket']} <b>Выберите действие:</b>
"""
    
    try:
        bot.edit_message_text(
            welcome_text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception as e:
        # Если не удалось отредактировать, отправляем новое
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

# Остальные функции остаются без изменений, но с добавлением декоратора @handle_error
# и использованием новых сервисов вместо прямого обращения к DATA

@handle_error
def show_subscription_options(message):
    """Показать варианты подписок"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['subscription']} 1 месяц - 109 ₽", callback_data="subscribe_1"),
        types.InlineKeyboardButton(f"{EMOJI['subscription']} 3 месяца - 319 ₽", callback_data="subscribe_3"),
        types.InlineKeyboardButton(f"{EMOJI['subscription']} 6 месяцев - 628 ₽", callback_data="subscribe_6"),
        types.InlineKeyboardButton(f"{EMOJI['subscription']} 12 месяцев - 999 ₽", callback_data="subscribe_12"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main")
    )
    
    text = f"""
{EMOJI['subscription']} <b>Выберите тарифный план:</b>

<b>1 месяц</b> - 109 ₽
<b>3 месяца</b> - 319 ₽ (скидка 3%)
<b>6 месяцев</b> - 628 ₽ (скидка 4%)
<b>12 месяцев</b> - 999 ₽ (скидка 24%)

{EMOJI['device']} <b>Лимит устройств:</b> 3
{EMOJI['speed']} <b>Скорость:</b> Без ограничений
{EMOJI['security']} <b>Безопасность:</b> Военный уровень
{EMOJI['no_logs']} <b>Логи:</b> Не ведем
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

# Добавлю остальные функции с улучшениями...

@handle_error
def show_balance_menu(message):
    """Показать меню баланса"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['payment']} Пополнить баланс", callback_data="top_up_balance"),
        types.InlineKeyboardButton(f"{EMOJI['history']} История пополнения", callback_data="payment_history"),
        types.InlineKeyboardButton(f"{EMOJI['coupon']} Активировать купон", callback_data="activate_coupon"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Вернуться в личный кабинет", callback_data="back_to_main")
    )
    
    # Получаем актуальный баланс
    user_stats = user_service.get_user_stats(message.from_user.id)
    balance = user_stats.get('balance_rub', 0)
    days = user_stats.get('days_remaining', 0)
    
    text = f"""
{EMOJI['balance']} <b>Баланс:</b> {balance} ₽  (≈ {days} дн.)

{EMOJI['info']} <b>Доступные действия:</b>

{EMOJI['payment']} <b>Пополнить баланс</b> — Добавить средства на счет
{EMOJI['history']} <b>История пополнения</b> — Посмотреть транзакции
{EMOJI['coupon']} <b>Активировать купон</b> — Ввести промокод
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

# Добавлю остальные функции...

if __name__ == "__main__":
    logger.info("Запуск улучшенного бота...")
    
    # Проверяем доступность Marzban API
    if not marzban_service.health_check():
        logger.warning("Marzban API недоступен, но бот продолжает работу")
    
    # Попытка запуска с обработкой конфликта
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            bot.polling(none_stop=True)
            break
        except Exception as e:
            if "Conflict: terminated by other getUpdates request" in str(e):
                retry_count += 1
                logger.warning(f"Другой экземпляр бота уже запущен. Попытка {retry_count}/{max_retries}")
                if retry_count < max_retries:
                    time.sleep(10)  # Ждем 10 секунд перед следующей попыткой
                else:
                    logger.error("Не удалось запустить бота после нескольких попыток")
                    sys.exit(1)
            else:
                logger.error(f"Ошибка при запуске бота: {e}")
                sys.exit(1)