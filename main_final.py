#!/usr/bin/env python3
"""
Финальная улучшенная версия Telegram Bot для пользователей Marzban
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
from src.utils.error_handler import init_error_handler, get_error_handler
from src.utils.qr_generator import qr_generator

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

# Инициализация обработчика ошибок
init_error_handler(bot)

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

# Декоратор для обработки ошибок
def handle_error(context: str = "", user_friendly_error: str = "general"):
    """Декоратор для обработки ошибок"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler = get_error_handler()
                user_id = None
                if args and hasattr(args[0], 'from_user'):
                    user_id = args[0].from_user.id
                elif args and hasattr(args[0], 'chat'):
                    user_id = args[0].chat.id
                
                error_handler.handle_error(e, context, user_id)
                if user_id:
                    error_handler.send_user_error(user_id, user_friendly_error)
                return None
        return wrapper
    return decorator

@bot.message_handler(commands=['start'])
@handle_error("start_command", "general")
def start_command(message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username
    
    logger.info(f"Команда /start: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Создаем или получаем запись пользователя
    user = user_service.ensure_user_record(user_id, username, first_name)
    
    # Обрабатываем реферальный параметр
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
    
    # Если это первый /start — показываем приветствие
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
    
    # Показываем главное меню
    show_main_menu(message)

@bot.callback_query_handler(func=lambda call: True)
@handle_error("callback_handler", "general")
def handle_callback(call):
    """Обработчик всех callback запросов"""
    class FakeMessage:
        def __init__(self, call):
            self.chat = call.message.chat
            self.message_id = call.message.message_id
            self.from_user = call.from_user
    
    fake_message = FakeMessage(call)
    
    # Маршрутизация callback'ов
    if call.data == "add_subscription":
        show_subscription_options(fake_message)
    elif call.data == "my_subscriptions":
        show_my_subscriptions(fake_message)
    elif call.data == "balance":
        show_balance_menu(fake_message)
    elif call.data.startswith("get_test_"):
        username = call.data.replace("get_test_", "")
        get_test_period(fake_message, username)
    elif call.data == "invite_friend":
        show_invite_menu(fake_message)
    elif call.data == "my_referrals":
        show_referrals_menu(fake_message)
    elif call.data == "about_service":
        show_about_service(fake_message)
    elif call.data == "back_to_main":
        show_main_menu(fake_message)
    elif call.data.startswith("subscribe_"):
        handle_subscription_purchase(fake_message, call.data)
    elif call.data == "top_up_balance":
        show_payment_options(fake_message)
    elif call.data == "payment_history":
        show_payment_history(fake_message)
    elif call.data == "activate_coupon":
        activate_coupon(fake_message)
    elif call.data == "share_link":
        share_referral_link(fake_message)
    elif call.data == "show_qr":
        show_qr_code(fake_message)
    elif call.data == "support_chat":
        show_support_chat(fake_message)
    elif call.data == "channel_link":
        show_channel_link(fake_message)
    elif call.data == 'start_setup':
        show_setup_step1(fake_message)
    elif call.data.startswith('choose_device_'):
        device_key = call.data.replace('choose_device_', '')
        show_setup_step2(fake_message, device_key)
    elif call.data == 'continue_setup':
        continue_setup_flow(fake_message)
    elif call.data == 'back_to_setup_1':
        show_setup_step1(fake_message)
    elif call.data == 'finish_setup':
        finish_setup(fake_message)
    elif call.data == 'show_qr_key':
        show_qr_key(fake_message)
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
    
    # Отвечаем на callback query
    try:
        bot.answer_callback_query(call.id)
    except Exception as e:
        logger.warning(f"Ошибка ответа на callback query: {e}")

@handle_error("show_main_menu", "general")
def show_main_menu(message):
    """Показать главное меню"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "Пользователь"
    
    if not username:
        username = first_name.lower().replace(" ", "_")
    
    logger.info(f"Главное меню: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Проверяем подписку
    user_info = marzban_service.get_user_info(username) if username else None
    is_new_user = user_id not in test_users
    
    # Получаем статистику пользователя
    user_stats = user_service.get_user_stats(user_id)
    
    # Создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    if user_info:
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['add']} Продлить подписку", callback_data="add_subscription"),
            types.InlineKeyboardButton(f"{EMOJI['subscription']} Мои подписки", callback_data="my_subscriptions")
        )
    elif is_new_user:
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['gift']} Получить тестовый период", callback_data=f"get_test_{username}"),
            types.InlineKeyboardButton(f"{EMOJI['subscription']} Мои подписки", callback_data="my_subscriptions")
        )
    else:
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['add']} Купить подписку", callback_data="add_subscription"),
            types.InlineKeyboardButton(f"{EMOJI['subscription']} Мои подписки", callback_data="my_subscriptions")
        )
    
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['balance']} Баланс", callback_data="balance"))
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['referral']} Пригласить друга", callback_data="invite_friend"),
        types.InlineKeyboardButton(f"{EMOJI['referral']} Мои рефералы", callback_data="my_referrals")
    )
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['info']} О сервисе", callback_data="about_service"))
    
    # Формируем текст
    balance = user_stats.get('balance_rub', 0)
    days = user_stats.get('days_remaining', 0)
    
    if user_info:
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
    except Exception:
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

# Добавлю остальные функции с улучшениями...

@handle_error("show_balance_menu", "general")
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

@handle_error("show_invite_menu", "general")
def show_invite_menu(message):
    """Показать меню приглашений с QR-кодом"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    ref_user_id = message.from_user.id
    share_link = f"https://t.me/{bot.get_me().username}?start=ref_{ref_user_id}"
    
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['share']} Поделиться ссылкой", url=f"https://t.me/share/url?url={share_link}&text=Присоединяйся к YoVPN!"),
        types.InlineKeyboardButton(f"{EMOJI['qr']} Показать QR-код", callback_data="show_qr"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main")
    )
    
    # Получаем статистику рефералов
    user_stats = user_service.get_user_stats(ref_user_id)
    ref_count = user_stats.get('referrals_count', 0)
    income = user_stats.get('referral_income', 0)
    
    text = f"""
{EMOJI['referral']} <b>Реферальная система</b>

{EMOJI['info']} <b>Ваша статистика:</b>
• Приглашено: {ref_count} человек(а)
• Доход с рефералов: {income} ₽ (10 ₽ + 2 ₽ бонус/чел)

{EMOJI['link']} <b>Ваша реферальная ссылка:</b>
{share_link}
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error("show_qr_code", "general")
def show_qr_code(message):
    """Показать QR-код для реферальной ссылки"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="invite_friend"))
    
    ref_user_id = message.from_user.id
    share_link = f"https://t.me/{bot.get_me().username}?start=ref_{ref_user_id}"
    
    # Генерируем QR-код
    qr_code = qr_generator.generate_referral_qr(share_link)
    
    if qr_code:
        try:
            bot.send_photo(
                message.chat.id,
                photo=qr_code,
                caption=f"{EMOJI['qr']} <b>QR-код реферальной ссылки</b>\n\n{EMOJI['info']} Отсканируйте QR-код для быстрого доступа к реферальной ссылке",
                parse_mode='HTML',
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка отправки QR-кода: {e}")
            bot.send_message(
                message.chat.id,
                f"{EMOJI['qr']} <b>QR-код реферальной ссылки</b>\n\n{EMOJI['link']} <b>Ваша ссылка:</b>\n<code>{share_link}</code>",
                parse_mode='HTML',
                reply_markup=keyboard
            )
    else:
        bot.send_message(
            message.chat.id,
            f"{EMOJI['qr']} <b>QR-код реферальной ссылки</b>\n\n{EMOJI['link']} <b>Ваша ссылка:</b>\n<code>{share_link}</code>",
            parse_mode='HTML',
            reply_markup=keyboard
        )

# Добавлю остальные функции...

@handle_error("show_about_service", "general")
def show_about_service(message):
    """Показать информацию о сервисе"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['support']} Поддержка", callback_data="support_chat"),
        types.InlineKeyboardButton(f"{EMOJI['channel']} Канал", callback_data="channel_link"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Личный кабинет", callback_data="back_to_main")
    )
    
    text = f"""
{EMOJI['info']} <b>О сервисе</b>

<b>Наши преимущества:</b>
• Высокая скорость соединения
• Военная защита данных
• Полное отсутствие логов
• Стабильная работа 24/7
• Поддержка всех устройств

{EMOJI['device']} <b>Поддерживаемые платформы:</b>
• Windows, macOS, Linux
• iOS, Android
• Router, Smart TV

{EMOJI['security']} <b>Протоколы:</b>
• V2Ray, Clash, Sing-box
• Outline, Shadowsocks
• WireGuard, OpenVPN

{EMOJI['support']} <b>Техподдержка:</b> @icewhipe
{EMOJI['channel']} <b>Канал:</b> @yodevelop
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

# Добавлю остальные функции с заглушками...

@handle_error("show_subscription_options", "general")
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

# Заглушки для остальных функций
def show_my_subscriptions(message):
    bot.send_message(message.chat.id, f"{EMOJI['subscription']} <b>Мои подписки</b>\n\n{EMOJI['warning']} Функция в разработке")

def get_test_period(message, username):
    bot.send_message(message.chat.id, f"{EMOJI['gift']} <b>Тестовый период</b>\n\n{EMOJI['warning']} Функция в разработке")

def show_referrals_menu(message):
    bot.send_message(message.chat.id, f"{EMOJI['referral']} <b>Мои рефералы</b>\n\n{EMOJI['warning']} Функция в разработке")

def handle_subscription_purchase(message, callback_data):
    bot.send_message(message.chat.id, f"{EMOJI['payment']} <b>Покупка подписки</b>\n\n{EMOJI['warning']} Платежная система скоро будет доступна")

def show_payment_options(message):
    bot.send_message(message.chat.id, f"{EMOJI['payment']} <b>Пополнение баланса</b>\n\n{EMOJI['warning']} Платежная система скоро будет доступна")

def show_payment_history(message):
    bot.send_message(message.chat.id, f"{EMOJI['history']} <b>История платежей</b>\n\n{EMOJI['warning']} Функция в разработке")

def activate_coupon(message):
    bot.send_message(message.chat.id, f"{EMOJI['coupon']} <b>Активация купона</b>\n\n{EMOJI['warning']} Функция в разработке")

def share_referral_link(message):
    bot.send_message(message.chat.id, f"{EMOJI['share']} <b>Поделиться ссылкой</b>\n\n{EMOJI['warning']} Функция в разработке")

def show_support_chat(message):
    bot.send_message(message.chat.id, f"{EMOJI['support']} <b>Поддержка</b>\n\n{EMOJI['info']} Свяжитесь с нами: @icewhipe")

def show_channel_link(message):
    bot.send_message(message.chat.id, f"{EMOJI['channel']} <b>Наш канал</b>\n\n{EMOJI['info']} Подписывайтесь: @yodevelop")

def show_setup_step1(message):
    bot.send_message(message.chat.id, f"{EMOJI['settings']} <b>Настройка VPN</b>\n\n{EMOJI['warning']} Функция в разработке")

def show_setup_step2(message, device_key):
    bot.send_message(message.chat.id, f"{EMOJI['settings']} <b>Настройка для {device_key}</b>\n\n{EMOJI['warning']} Функция в разработке")

def continue_setup_flow(message):
    bot.send_message(message.chat.id, f"{EMOJI['settings']} <b>Продолжение настройки</b>\n\n{EMOJI['warning']} Функция в разработке")

def finish_setup(message):
    bot.send_message(message.chat.id, f"{EMOJI['check']} <b>Настройка завершена</b>\n\n{EMOJI['info']} Добро пожаловать!")

def show_qr_key(message):
    bot.send_message(message.chat.id, f"{EMOJI['qr']} <b>QR-код ключа</b>\n\n{EMOJI['warning']} Функция в разработке")

def show_vpn_links(message, username):
    bot.send_message(message.chat.id, f"{EMOJI['link']} <b>VPN ссылки</b>\n\n{EMOJI['warning']} Функция в разработке")

def show_vless_links(message, username):
    bot.send_message(message.chat.id, f"{EMOJI['link']} <b>VLESS ссылки</b>\n\n{EMOJI['warning']} Функция в разработке")

def show_subscription_link(message, username):
    bot.send_message(message.chat.id, f"{EMOJI['link']} <b>Ссылка подписки</b>\n\n{EMOJI['warning']} Функция в разработке")

def copy_vless_link(message, callback_data):
    bot.send_message(message.chat.id, f"{EMOJI['link']} <b>Копирование ссылки</b>\n\n{EMOJI['warning']} Функция в разработке")

def get_vless_configs(message, username):
    bot.send_message(message.chat.id, f"{EMOJI['link']} <b>VLESS конфигурации</b>\n\n{EMOJI['warning']} Функция в разработке")

if __name__ == "__main__":
    logger.info("Запуск финальной версии бота...")
    
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
                    time.sleep(10)
                else:
                    logger.error("Не удалось запустить бота после нескольких попыток")
                    sys.exit(1)
            else:
                logger.error(f"Ошибка при запуске бота: {e}")
                sys.exit(1)