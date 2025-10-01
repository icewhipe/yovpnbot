#!/usr/bin/env python3
"""
Telegram Bot для пользователей Marzban
"""

import os
import sys
import logging
import time
import json
import threading
from io import BytesIO
from urllib.parse import quote
from decouple import config
import telebot
from telebot import types
from marzban_api import MarzbanAPI

# Опциональная поддержка генерации QR-кодов
try:
    import qrcode
    QR_AVAILABLE = True
except Exception:
    QR_AVAILABLE = False

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загрузка конфигурации
BOT_TOKEN = config('USERBOT_TOKEN', default='8385845645:AAGiZhSwkRgndegtTsy573Smnul2wFNwLu0')
MARZBAN_API_URL = config('MARZBAN_API_URL', default='https://alb-vpnprimex.duckdns.org:443/api')
MARZBAN_ADMIN_TOKEN = config('MARZBAN_ADMIN_TOKEN', default='')
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', default=3306, cast=int)
DB_NAME = config('DB_NAME', default='marzban')
DB_USER = config('DB_USER', default='marzban')
DB_PASSWORD = config('DB_PASSWORD', default='DcR92D5bNArCjVTpakf')

# Создание бота
bot = telebot.TeleBot(BOT_TOKEN)

# Инициализация Marzban API с токеном
marzban_api = MarzbanAPI(MARZBAN_API_URL, MARZBAN_ADMIN_TOKEN)

# Простое хранилище данных (JSON) для баланса/рефералок/настроек
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('DATA_DIR', BASE_DIR)
DATA_FILE = os.path.join(DATA_DIR, 'data.json')
DATA_LOCK = threading.Lock()

def _load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"users": {}}

def _save_data(data):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Не удалось сохранить данные: {e}")

DATA = _load_data()

def _sanitize_username(username, fallback_name):
    if username:
        return username
    return (fallback_name or "user").lower().replace(" ", "_")

def ensure_user_record(user_id, username, first_name):
    """Гарантированно создает запись пользователя в локальном хранилище."""
    global DATA
    with DATA_LOCK:
        data_users = DATA.setdefault("users", {})
        record = data_users.get(str(user_id))
        if not record:
            record = {
                "user_id": user_id,
                "username": _sanitize_username(username, first_name),
                "balance_rub": 0,
                "bonus_given": False,
                "first_start_completed": False,
                "referred_by": None,
                "referrals": [],
                "referrals_confirmed": [],
                "device": None,
                "app_link": None,
                "vless_link": None,
                "subscription_url": None
            }
            data_users[str(user_id)] = record
            _save_data(DATA)
        return record

def ensure_username_or_prompt(message) -> bool:
    """Проверяет наличие Telegram username. Если нет — показывает инструкцию и возвращает False."""
    if getattr(message.from_user, 'username', None):
        return True
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton("Проверить снова", callback_data='retry_start'))
    text = (
        f"{EMOJI['warning']} <b>Требуется Username</b>\n\n"
        f"Чтобы бот работал корректно, установите Username (ник) в Telegram.\n"
        f"Откройте: Настройки → Изменить профиль → Имя пользователя.\n\n"
        f"После установки нажмите «Проверить снова» или отправьте /start."
    )
    try:
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=keyboard)
    except Exception:
        pass
    return False

def get_user_record(user_id):
    with DATA_LOCK:
        return DATA.get("users", {}).get(str(user_id))

def update_user_record(user_id, updates: dict):
    global DATA
    with DATA_LOCK:
        if str(user_id) not in DATA.get("users", {}):
            return
        DATA["users"][str(user_id)].update(updates)
        _save_data(DATA)

def credit_balance(user_id, amount_rub, reason: str = ""):
    global DATA
    with DATA_LOCK:
        rec = DATA.get("users", {}).get(str(user_id))
        if not rec:
            return
        rec["balance_rub"] = max(0, int(rec.get("balance_rub", 0)) + int(amount_rub))
        _save_data(DATA)
    logger.info(f"Зачисление {amount_rub} ₽ пользователю {user_id}. Причина: {reason}")

def days_from_balance(balance_rub: int) -> int:
    try:
        return int(balance_rub) // 4
    except Exception:
        return 0

def find_user_id_by_username(username: str):
    with DATA_LOCK:
        for uid, rec in DATA.get("users", {}).items():
            if rec.get("username") == username:
                return int(uid)
    return None

def record_referral(referrer_user_id: int, referred_user_id: int):
    global DATA
    if referrer_user_id == referred_user_id:
        return False
    with DATA_LOCK:
        referrer = DATA.get("users", {}).get(str(referrer_user_id))
        referred = DATA.get("users", {}).get(str(referred_user_id))
        if not referrer or not referred:
            return False
        if referred.get("referred_by"):
            return False
        # Записываем связь и избегаем дублей
        referred["referred_by"] = referrer_user_id
        if str(referred_user_id) not in [str(x) for x in referrer.get("referrals", [])]:
            ref_list = referrer.get("referrals", [])
            ref_list.append(referred_user_id)
            referrer["referrals"] = ref_list
        # Начисление перенесено на момент активации ключа (confirm_referral_bonus)
        _save_data(DATA)
        logger.info(f"Реферал сохранен: {referrer_user_id} -> {referred_user_id}")
        return True

def confirm_referral_bonus(referred_user_id: int):
    """Начисляет 10 ₽ рефереру, когда реферал активировал ключ (создан конфиг)."""
    global DATA
    with DATA_LOCK:
        referred = DATA.get("users", {}).get(str(referred_user_id))
        if not referred:
            return False
        referrer_id = referred.get("referred_by")
        if not referrer_id:
            return False
        referrer = DATA.get("users", {}).get(str(referrer_id))
        if not referrer:
            return False
        # Избегаем повторного начисления
        already = str(referred_user_id) in [str(x) for x in referrer.get("referrals_confirmed", [])]
        if already:
            return False
        referrer["balance_rub"] = max(0, int(referrer.get("balance_rub", 0)) + 10)
        lst = referrer.get("referrals_confirmed", [])
        lst.append(referred_user_id)
        referrer["referrals_confirmed"] = lst
        _save_data(DATA)
        logger.info(f"Реферал подтвержден: {referrer_id} получил 10 ₽ за {referred_user_id}")
        return True

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

@bot.message_handler(commands=['start'])
def start_command(message):
    """Обработчик команды /start: приветствие, бонус, рефералка, начало настройки."""
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    # Требуем username
    if not ensure_username_or_prompt(message):
        return
    username = _sanitize_username(message.from_user.username, first_name)
    
    logger.info(f"Команда /start: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    record = ensure_user_record(user_id, username, first_name)
    
    # Обрабатываем реферальный параметр: /start ref_<id|username>
    try:
        param = None
        if message.text and ' ' in message.text:
            param = message.text.split(' ', 1)[1].strip()
        if param and param.startswith('ref_'):
            ref_key = param.replace('ref_', '', 1)
            referrer_id = int(ref_key) if ref_key.isdigit() else find_user_id_by_username(ref_key)
            if referrer_id:
                record_referral(referrer_id, user_id)
    except Exception as e:
        logger.warning(f"Не удалось обработать реферальный параметр: {e}")
    
    # Приветственный бонус теперь начисляется после успешной активации ключа (см. continue_setup_flow)
    
    # Если это самый первый /start — показываем приветствие с кнопкой настройки
    if not record.get('first_start_completed'):
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
        update_user_record(user_id, {"first_start_completed": True})
        return
    
    # Иначе показываем главное меню
    show_main_menu(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Обработчик всех callback запросов"""
    # Создаем объект message с правильными данными пользователя
    class FakeMessage:
        def __init__(self, call):
            self.chat = call.message.chat
            self.message_id = call.message.message_id
            self.from_user = call.from_user  # Используем call.from_user, а не call.message.from_user
    
    fake_message = FakeMessage(call)
    
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
        if ensure_username_or_prompt(fake_message):
            show_setup_step1(fake_message)
    elif call.data.startswith('choose_device_'):
        if ensure_username_or_prompt(fake_message):
            device_key = call.data.replace('choose_device_', '')
            show_setup_step2(fake_message, device_key)
    elif call.data == 'continue_setup':
        if ensure_username_or_prompt(fake_message):
            continue_setup_flow(fake_message)
    elif call.data == 'back_to_setup_1':
        if ensure_username_or_prompt(fake_message):
            show_setup_step1(fake_message)
    elif call.data == 'finish_setup':
        if ensure_username_or_prompt(fake_message):
            finish_setup(fake_message)
    elif call.data == 'show_qr_key':
        if ensure_username_or_prompt(fake_message):
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
    
    # Отвечаем на callback query сразу
    try:
        bot.answer_callback_query(call.id)
    except:
        pass  # Игнорируем ошибки callback query

def show_main_menu(message):
    """Показать главное меню (для редактирования сообщений)"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "Пользователь"
    
    # Если username None, используем first_name
    if not username:
        username = first_name.lower().replace(" ", "_")
    
    logger.info(f"Главное меню: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Синхронизируем срок действия с балансом (каждые 4 ₽ = 1 день)
    user_rec = ensure_user_record(user_id, username, first_name)
    try:
        marzban_api.apply_balance_as_days(username, int(user_rec.get('balance_rub', 0)))
    except Exception:
        pass
    # Проверяем, есть ли у пользователя подписка
    user_info = marzban_api.get_user_info(username) if username else None
    is_new_user = user_id not in test_users
    
    # Создаем клавиатуру главного меню
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Верхний ряд: балансная модель
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['subscription']} Мои подписки", callback_data="my_subscriptions"),
        types.InlineKeyboardButton(f"{EMOJI['settings']} Настроить VPN", callback_data='start_setup')
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
    
    if user_info:
        # Пользователь с подпиской
        welcome_text = f"""
{EMOJI['user']} <b>Добро пожаловать, {first_name}!</b>

<b>Ваш профиль:</b>
├ ID: {user_id}
├ Username: @{username}
├ Баланс: 0 RUB
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
├ Баланс: 0 RUB
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
├ Баланс: 0 RUB
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

def show_subscription_options(message):
    """Балансная модель: рассказываем как пополнить и что 4 ₽ = 1 день."""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['balance']} Пополнить баланс", callback_data="top_up_balance"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main")
    )

    text = f"""
{EMOJI['subscription']} <b>Подписка по балансу</b>

{EMOJI['info']} Каждые 4 ₽ = 1 день подписки.\n
Пополняйте баланс на любую сумму — срок действия автоматически применяется.

{EMOJI['speed']} Безлимитная скорость\n{EMOJI['no_logs']} Без логов\n{EMOJI['security']} Защита уровня VLESS (Reality)
"""

    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def get_test_period(message, username):
    """Получить тестовый период с анимацией (отключено в балансной модели)."""
    import time
    import threading
    
    user_id = message.from_user.id
    
    def animate_creation():
        """Анимация создания VPN аккаунта"""
        stages = [
            {
                "text": f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['hourglass']} <b>Инициализация системы...</b>

{EMOJI['loading']} Подключаемся к серверам
""",
                "duration": 3
            },
            {
                "text": f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['hourglass']} <b>Генерируем уникальный ID...</b>

{EMOJI['loading']} Создаем безопасное соединение
""",
                "duration": 4
            },
            {
                "text": f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['hourglass']} <b>Настраиваем VPN протокол...</b>

{EMOJI['loading']} Активируем VLESS с Reality
""",
                "duration": 5
            },
            {
                "text": f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['hourglass']} <b>Выделяем ресурсы...</b>

{EMOJI['loading']} Настраиваем безлимитный трафик
""",
                "duration": 4
            },
            {
                "text": f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['hourglass']} <b>Создаем аккаунт...</b>

{EMOJI['loading']} Устанавливаем срок действия 7 дней
""",
                "duration": 4
            },
            {
                "text": f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['hourglass']} <b>Финальная настройка...</b>

{EMOJI['loading']} Проверяем безопасность соединения
""",
                "duration": 5
            },
            {
                "text": f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['hourglass']} <b>Активация аккаунта...</b>

{EMOJI['loading']} Готовим ссылки для подключения
""",
                "duration": 4
            }
        ]
        
        for stage in stages:
            try:
                bot.edit_message_text(
                    stage["text"],
                    message.chat.id,
                    message.message_id,
                    parse_mode='HTML'
                )
            except:
                pass
            time.sleep(stage["duration"])
    
    # Запускаем анимацию в отдельном потоке
    animation_thread = threading.Thread(target=animate_creation)
    animation_thread.start()
    
    # Ждем завершения анимации
    animation_thread.join()
    
    # Отключено: бесплатный тест не предоставляется повторно и в балансной модели не показывается
    test_user = None
    
    if test_user:
        # Тестовый аккаунт создан - показываем успех
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['link']} Получить ссылку", callback_data=f"get_link_{username}"))
        
        success_text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['cross']} <b>Бесплатный тест отключен</b>

{EMOJI['info']} Пополняйте баланс: каждые 4 ₽ = 1 день.
"""
    else:
        # Ошибка создания
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['add']} Купить подписку", callback_data="add_subscription"),
            types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main")
        )
        
        success_text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['info']} Пополняйте баланс: каждые 4 ₽ = 1 день. Нажмите «Настроить VPN» для получения ключа.
"""
    
    try:
        bot.edit_message_text(
            success_text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except:
        bot.send_message(
            message.chat.id,
            success_text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

def show_setup_step1(message):
    """Шаг 1: Выбор устройства"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("iOS", callback_data='choose_device_ios'),
        types.InlineKeyboardButton("Android", callback_data='choose_device_android')
    )
    keyboard.add(
        types.InlineKeyboardButton("Windows", callback_data='choose_device_windows'),
        types.InlineKeyboardButton("macOS", callback_data='choose_device_macos')
    )
    keyboard.add(
        types.InlineKeyboardButton("AndroidTV", callback_data='choose_device_androidtv')
    )
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data='back_to_main')
    )

    text = (
        f"{EMOJI['settings']} <b>Шаг 1.</b> Выберите тип устройства\n\n"
        f"Доступные варианты: iOS, Android, Windows, macOS, AndroidTV"
    )

    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception:
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=keyboard)

DEVICE_APP_LINKS = {
    "ios": "https://apps.apple.com/ru/app/v2raytun/id6476628951?l=en-GB",
    "android": "https://play.google.com/store/apps/details?id=app.hiddify.com&hl=ru",
    "windows": "https://github.com/hiddify/hiddify-app/releases/latest/download/Hiddify-Windows-Setup-x64.Msix",
    "macos": "https://apps.apple.com/ru/app/v2raytun/id6476628951?l=en-GB",
    "androidtv": "https://play.google.com/store/apps/details?id=app.hiddify.com&hl=ru"
}

def _device_human_name(key: str) -> str:
    mapping = {
        "ios": "iOS",
        "android": "Android",
        "windows": "Windows",
        "macos": "macOS",
        "androidtv": "AndroidTV"
    }
    return mapping.get(key, key)

def show_setup_step2(message, device_key: str):
    """Шаг 2: Установка приложения для выбранного устройства"""
    device_key = device_key.lower()
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username or first_name.lower().replace(" ", "_")

    ensure_user_record(user_id, username, first_name)

    app_link = DEVICE_APP_LINKS.get(device_key)
    update_user_record(user_id, {"device": device_key, "app_link": app_link})

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if app_link:
        keyboard.add(types.InlineKeyboardButton(f"Скачать для {_device_human_name(device_key)}", url=app_link))
    keyboard.add(
        types.InlineKeyboardButton("Продолжить настройку VPN", callback_data='continue_setup'),
        types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data='back_to_setup_1')
    )

    text = (
        f"{EMOJI['settings']} <b>Шаг 2.</b> Установите приложение для {_device_human_name(device_key)}\n\n"
        f"После установки нажмите «Продолжить настройку VPN»."
    )

    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception:
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=keyboard)

def continue_setup_flow(message):
    """Шаг 3: Анимация и генерация VLESS-конфига (Marzban)"""
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username or first_name.lower().replace(" ", "_")

    stages = [
        (f"{EMOJI['hourglass']} <b>Готовим инфраструктуру...</b>\n\n{EMOJI['loading']} Подключаемся к серверам", 2),
        (f"{EMOJI['hourglass']} <b>Настраиваем протокол...</b>\n\n{EMOJI['loading']} Активируем VLESS Reality", 3),
        (f"{EMOJI['hourglass']} <b>Создаем ваш ключ...</b>\n\n{EMOJI['loading']} Генерируем доступ", 3)
    ]
    for text, delay in stages:
        try:
            bot.edit_message_text(text, message.chat.id, message.message_id, parse_mode='HTML')
        except Exception:
            msg = bot.send_message(message.chat.id, text, parse_mode='HTML')
            message = msg
        time.sleep(delay)

    user_info = marzban_api.get_user_info(username)
    if not user_info:
        try:
            marzban_api.create_test_user(username, message.from_user.id)
            user_info = marzban_api.get_user_info(username)
        except Exception as e:
            logger.error(f"Не удалось создать пользователя в Marzban: {e}")

    vless_link = None
    sub_url = None
    if user_info and isinstance(user_info, dict):
        links = user_info.get('links') or []
        if links:
            vless_link = links[0]
        sub_url = user_info.get('subscription_url')

    update_user_record(message.from_user.id, {"vless_link": vless_link, "subscription_url": sub_url})

    # Начисляем приветственный бонус только при успешном получении ключа
    if vless_link and not get_user_record(message.from_user.id).get('bonus_given'):
        credit_balance(message.from_user.id, 20, reason='welcome_bonus_after_activation')
        update_user_record(message.from_user.id, {"bonus_given": True})
        # Подтверждаем реферальный бонус (10 ₽) рефереру
        confirm_referral_bonus(message.from_user.id)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Завершить настройку", callback_data='finish_setup'),
        types.InlineKeyboardButton("Показать в виде QR-кода", callback_data='show_qr_key')
    )

    text_lines = [
        f"{EMOJI['check']} <b>Шаг 3.</b> Подписка готова!",
        "",
    ]
    if sub_url:
        text_lines.extend([
            f"{EMOJI['subscription']} <b>Ваша подписка:</b>",
            f"<code>{sub_url}</code>",
            "",
            f"{EMOJI['info']} Импортируйте ссылку в приложение. Клиент сам обновляет узлы.",
        ])
    else:
        text_lines.append(f"{EMOJI['cross']} Не удалось получить ссылку-подписку. Попробуйте позже или обратитесь в поддержку.")

    final_text = "\n".join(text_lines)
    try:
        bot.edit_message_text(final_text, message.chat.id, message.message_id, parse_mode='HTML', reply_markup=keyboard)
    except Exception:
        bot.send_message(message.chat.id, final_text, parse_mode='HTML', reply_markup=keyboard)

def show_qr_key(message):
    """Показать QR-код для ссылки-подписки"""
    first_name = message.from_user.first_name or "Пользователь"
    username = message.from_user.username or first_name.lower().replace(" ", "_")
    user_info = marzban_api.get_user_info(username)
    sub_url = None
    if user_info and isinstance(user_info, dict):
        sub_url = user_info.get('subscription_url')
    if not sub_url:
        rec = get_user_record(message.from_user.id)
        sub_url = rec.get('subscription_url') if rec else None

    if not sub_url:
        bot.send_message(message.chat.id, f"{EMOJI['cross']} Подписка не найдена. Попробуйте заново.")
        return

    if QR_AVAILABLE:
        try:
            img = qrcode.make(sub_url)
            bio = BytesIO()
            img.save(bio, format='PNG')
            bio.seek(0)
            kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data='finish_setup'))
            bot.send_photo(message.chat.id, photo=bio, caption=f"{EMOJI['qr']} QR-код вашей подписки", reply_markup=kb)
            return
        except Exception as e:
            logger.warning(f"Не удалось сгенерировать QR локально: {e}")

    # Fallback: отдать QR как URL-сервис
    try:
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=512x512&data={quote(sub_url)}"
        kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data='finish_setup'))
        bot.send_photo(message.chat.id, photo=qr_url, caption=f"{EMOJI['qr']} QR-код вашей подписки", reply_markup=kb)
        return
    except Exception as e:
        logger.warning(f"Не удалось отправить QR через сервис: {e}")

    bot.send_message(message.chat.id, f"{EMOJI['qr']} Ваша подписка:\n<code>{sub_url}</code>", parse_mode='HTML')

def finish_setup(message):
    """Завершение настройки: конфетти и главное меню"""
    try:
        bot.edit_message_text("🎉 Настройка завершена!", message.chat.id, message.message_id)
    except Exception:
        bot.send_message(message.chat.id, "🎉 Настройка завершена!")
    show_main_menu(message)

def show_my_subscriptions(message):
    """Показать мои подписки"""
    keyboard = types.InlineKeyboardMarkup()
    
    # Получаем username из сообщения
    username = message.from_user.username
    if not username:
        username = (message.from_user.first_name or "Пользователь").lower().replace(" ", "_")
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    
    logger.info(f"Пользователь: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Username нормализован
    
    logger.info(f"Ищем пользователя в Marzban: {username}")
    
    # Получаем данные пользователя из Marzban
    user_info = marzban_api.get_user_info(username)
    
    if not user_info:
        # Нет данных о подписке — предлагаем начать настройку
        keyboard.add(
            types.InlineKeyboardButton(f"{EMOJI['settings']} Настроить VPN", callback_data='start_setup'),
            types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data='back_to_main')
        )
        text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['cross']} Активной конфигурации нет. Нажмите «Настроить VPN» чтобы получить ключ.
"""
    else:
        # Пользователь найден - показываем его данные
        status = user_info['status']
        days_remaining = user_info['days_remaining']
        traffic = user_info['traffic']
        links = user_info['links']
        subscription_url = user_info['subscription_url']
        
        # Определяем статус и эмодзи
        if status == 'active':
            status_emoji = EMOJI['active']
            status_text = "🟢 Активна"
        elif status == 'expired':
            status_emoji = EMOJI['expired']
            status_text = "🔴 Истекла"
        elif status == 'limited':
            status_emoji = EMOJI['limited']
            status_text = "🟡 Трафик исчерпан"
        else:
            status_emoji = EMOJI['cross']
            status_text = "⚫ Неактивна"
        
        # Форматируем трафик
        used_traffic = marzban_api.format_traffic(traffic['used'])
        if traffic['limit'] == "∞":
            limit_traffic = "∞"
            traffic_percent = 0
        else:
            limit_traffic = marzban_api.format_traffic(traffic['limit'])
            traffic_percent = traffic['percent']
        
        # Добавляем кнопки по порядку
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['link']} Получить ссылку", callback_data=f"get_link_{username}"))
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['add']} Продлить", callback_data="add_subscription"))
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
        
        # Формируем текст с красивым оформлением
        text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{status_emoji} <b>Статус:</b> {status_text}
{EMOJI['device']} <b>Устройства:</b> 0/3
{EMOJI['warning']} <b>Трафик:</b> {used_traffic} / {limit_traffic} ({traffic_percent}%)

{EMOJI['info']} <b>Дней осталось:</b> {days_remaining if days_remaining != 999 else '∞'}

{EMOJI['link']} <b>Доступные ссылки:</b>
• VLESS: {len(links)} серверов
• Подписка: Готова к установке
"""
    
    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception as e:
        # Если сообщение не изменилось, отправляем новое
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

def show_vpn_links(message, username):
    """Показать ссылки VPN для пользователя"""
    keyboard = types.InlineKeyboardMarkup()
    
    # Получаем данные пользователя
    user_info = marzban_api.get_user_info(username)
    
    if not user_info:
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="my_subscriptions"))
        text = f"""
{EMOJI['cross']} <b>Пользователь не найден</b>

{EMOJI['info']} Обратитесь к администратору
"""
    else:
        links = user_info['links']
        subscription_url = user_info['subscription_url']
        
        # В балансной модели показываем только подписку
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['subscription']} Подписка", callback_data=f"show_sub_{username}"))
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="my_subscriptions"))
        
        text = f"""
{EMOJI['link']} <b>Ссылки для установки VPN</b>

{EMOJI['rocket']} <b>Доступно:</b>
• Подписка: Готова к установке

{EMOJI['info']} <b>О подписке:</b>
• Одна ссылка на наш домен, внутри клиент сам обновляет список узлов

{EMOJI['device']} <b>Рекомендуемые приложения:</b>
• iOS/macOS: v2raytun
• Android/Windows/AndroidTV: Hiddify
"""
    
    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка редактирования сообщения: {e}")
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

def get_vless_configs(message, username):
    """Получить VLESS конфигурации"""
    user_info = marzban_api.get_user_info(username)
    
    if not user_info:
        text = f"{EMOJI['cross']} Пользователь не найден"
    else:
        links = user_info['links']
        
        text = f"""
{EMOJI['link']} <b>VLESS конфигурации</b>

{EMOJI['rocket']} <b>Доступные серверы:</b>
"""
        
        for i, link in enumerate(links[:5]):
            server_name = f"Сервер {i+1}"
            if "Албания" in link:
                server_name = "🇦🇱 Албания"
            elif "Нидерланды" in link:
                server_name = "🇳🇱 Нидерланды"
            
            text += f"• {server_name}\n"
        
        text += f"""
{EMOJI['info']} <b>Инструкция по установке:</b>
1. Скопируйте ссылку сервера
2. Откройте приложение V2rayNG/Clash
3. Добавьте конфигурацию
4. Подключитесь к серверу

{EMOJI['rocket']} <b>Готово! Ваш VPN активен</b>
"""
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=f"show_vless_{username}"))
    
    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except:
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

def show_vless_links(message, username):
    """Показать VLESS ссылки"""
    keyboard = types.InlineKeyboardMarkup()
    
    user_info = marzban_api.get_user_info(username)
    
    if not user_info:
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="my_subscriptions"))
        text = f"{EMOJI['cross']} Пользователь не найден"
    else:
        links = user_info['links']
        
        # Добавляем кнопку для получения конфигураций
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['link']} Получить конфигурации", callback_data=f"get_configs_{username}"))
        
        # Добавляем кнопки для каждого сервера
        for i, link in enumerate(links[:5]):  # Показываем максимум 5 ссылок
            server_name = f"Сервер {i+1}"
            if "Албания" in link:
                server_name = "🇦🇱 Албания"
            elif "Нидерланды" in link:
                server_name = "🇳🇱 Нидерланды"
            
            keyboard.add(
                types.InlineKeyboardButton(f"{EMOJI['link']} {server_name}", callback_data=f"copy_link_{i}")
            )
        
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=f"get_link_{username}"))
        
        text = f"""
{EMOJI['link']} <b>VLESS ссылки</b>

{EMOJI['rocket']} <b>Доступные серверы:</b>
• 🇦🇱 Албания - быстрый и стабильный
• 🇳🇱 Нидерланды - европейский сервер

{EMOJI['info']} <b>Выберите сервер для копирования ссылки</b>

{EMOJI['device']} <b>Как использовать:</b>
1. Нажмите на сервер
2. Скопируйте ссылку
3. Вставьте в VPN приложение
"""
    
    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка редактирования сообщения: {e}")
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

def show_subscription_link(message, username):
    """Показать ссылку на подписку"""
    keyboard = types.InlineKeyboardMarkup()
    
    user_info = marzban_api.get_user_info(username)
    
    if not user_info:
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="my_subscriptions"))
        text = f"{EMOJI['cross']} Пользователь не найден"
    else:
        subscription_url = user_info['subscription_url']
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=f"get_link_{username}"))
        
        text = f"""
{EMOJI['link']} <b>Ссылка на подписку</b>

{EMOJI['rocket']} <b>Подписка для автоматического обновления:</b>

<code>{subscription_url}</code>

{EMOJI['info']} <b>Как использовать:</b>
1. Скопируйте ссылку выше
2. Вставьте в VPN приложение
3. Приложение автоматически обновит серверы

{EMOJI['device']} <b>Поддерживаемые приложения:</b>
• Clash, Sing-box, Outline, v2rayNG
"""
    
    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка редактирования сообщения: {e}")
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

def copy_vless_link(message, callback_data):
    """Показать VLESS ссылку для копирования"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="my_subscriptions"))
    
    # Получаем username из сообщения
    username = message.from_user.username or message.from_user.first_name.lower().replace(" ", "_")
    user_info = marzban_api.get_user_info(username)
    
    if not user_info:
        text = f"{EMOJI['cross']} Пользователь не найден"
    else:
        links = user_info['links']
        link_index = int(callback_data.replace("copy_link_", ""))
        
        if link_index < len(links):
            vless_link = links[link_index]
            
            # Определяем название сервера
            server_name = "Сервер"
            if "Албания" in vless_link:
                server_name = "🇦🇱 Албания"
            elif "Нидерланды" in vless_link:
                server_name = "🇳🇱 Нидерланды"
            
            text = f"""
{EMOJI['link']} <b>{server_name}</b>

{EMOJI['rocket']} <b>VLESS ссылка:</b>

<code>{vless_link}</code>

{EMOJI['info']} <b>Как использовать:</b>
1. Скопируйте ссылку выше
2. Вставьте в VPN приложение
3. Подключитесь к серверу

{EMOJI['device']} <b>Поддерживаемые приложения:</b>
• v2rayNG, V2Box, Shadowrocket
• Clash, Sing-box, Outline
"""
        else:
            text = f"{EMOJI['cross']} Ссылка не найдена"
    
    try:
        bot.edit_message_text(
            text,
            message.chat.id,
            message.message_id,
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка редактирования сообщения: {e}")
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='HTML',
            reply_markup=keyboard
        )

def show_balance_menu(message):
    """Показать меню баланса"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['payment']} Пополнить баланс", callback_data="top_up_balance"),
        types.InlineKeyboardButton(f"{EMOJI['history']} История пополнения", callback_data="payment_history"),
        types.InlineKeyboardButton(f"{EMOJI['coupon']} Активировать купон", callback_data="activate_coupon"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Вернуться в личный кабинет", callback_data="back_to_main")
    )
    
    # Фактический баланс
    user_rec = get_user_record(message.from_user.id)
    balance = int(user_rec.get('balance_rub', 0)) if user_rec else 0
    days = days_from_balance(balance)
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

def show_invite_menu(message):
    """Показать меню приглашений"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    ref_user_id = message.from_user.id
    share_link = f"https://t.me/{bot.get_me().username}?start=ref_{ref_user_id}"
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['share']} Поделиться ссылкой", url=f"https://t.me/share/url?url={share_link}&text=Присоединяйся к YoVPN!"),
        types.InlineKeyboardButton(f"{EMOJI['qr']} Показать QR-код", callback_data="show_qr"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main")
    )
    
    rec = get_user_record(ref_user_id)
    ref_count = len(rec.get('referrals', [])) if rec else 0
    income = ref_count * 12
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

def show_referrals_menu(message):
    """Показать мои рефералы"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
    
    rec = get_user_record(message.from_user.id)
    ref_list = rec.get('referrals', []) if rec else []
    income = len(ref_list) * 12
    if not ref_list:
        text = f"""
{EMOJI['referral']} <b>Мои рефералы</b>

{EMOJI['cross']} Рефералов пока нет.
{EMOJI['info']} Делитесь своей ссылкой в «Пригласить друга».\nЗа каждого — 10 ₽ + 2 ₽ бонус (3 дня).
"""
    else:
        lines = [f"{EMOJI['referral']} <b>Мои рефералы</b>", ""]
        lines.append(f"Всего: {len(ref_list)} | Доход: {income} ₽")
        text = "\n".join(lines)
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

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
• Windows, macOS
• iOS, Android, AndroidTV

{EMOJI['security']} <b>Протокол:</b>
• VLESS (Reality) — современный протокол, устойчивый к блокировкам и DPI.
  Шифрование и маскировка трафика обеспечивают стабильный доступ даже в сложных сетях.
  Приложения: v2raytun (iOS/macOS), Hiddify (Android/Windows/AndroidTV).

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

def handle_subscription_purchase(message, callback_data):
    """Обработка покупки подписки"""
    months = callback_data.split('_')[1]
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="add_subscription"))
    
    text = f"""
{EMOJI['subscription']} <b>Покупка подписки на {months} месяц(а)</b>

{EMOJI['warning']} Платежная система скоро будет доступна.

{EMOJI['support']} <b>Поддержка:</b> @icewhipe
{EMOJI['channel']} <b>Канал:</b> @yodevelop
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def show_payment_options(message):
    """Показать варианты оплаты"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="balance"))
    
    text = f"""
{EMOJI['payment']} <b>Пополнение баланса</b>

{EMOJI['warning']} Платежная система скоро будет доступна.

{EMOJI['support']} <b>Поддержка:</b> @icewhipe
{EMOJI['channel']} <b>Канал:</b> @yodevelop
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def show_payment_history(message):
    """Показать историю платежей"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="balance"))
    
    text = f"""
{EMOJI['history']} <b>История пополнения</b>

{EMOJI['cross']} <b>Транзакций пока нет</b>

{EMOJI['info']} <b>Здесь будут отображаться все ваши платежи</b>
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def activate_coupon(message):
    """Активация купона"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="balance"))
    
    text = f"""
{EMOJI['coupon']} <b>Активация купона</b>

{EMOJI['info']} <b>Отправьте промокод для активации</b>

{EMOJI['warning']} <b>Функция в разработке</b>
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def share_referral_link(message):
    """Поделиться реферальной ссылкой"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="invite_friend"))
    
    text = f"""
{EMOJI['share']} <b>Поделиться ссылкой</b>

{EMOJI['link']} <b>Ваша реферальная ссылка:</b>
https://t.me/{bot.get_me().username}?start=ref_{message.from_user.username}

{EMOJI['info']} <b>Поделитесь этой ссылкой с друзьями и получайте доход!</b>
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def show_qr_code(message):
    """Показать QR-код"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="invite_friend"))
    
    text = f"""
{EMOJI['qr']} <b>QR-код реферальной ссылки</b>

{EMOJI['warning']} <b>QR-код в разработке</b>

{EMOJI['info']} <b>Скоро здесь будет QR-код для быстрого доступа</b>
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def show_support_chat(message):
    """Показать чат поддержки"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="about_service"))
    
    text = f"""
{EMOJI['support']} <b>Поддержка</b>

{EMOJI['info']} <b>Свяжитесь с нами:</b>

{EMOJI['support']} <b>Техподдержка:</b> @icewhipe
{EMOJI['channel']} <b>Канал:</b> @yodevelop

{EMOJI['info']} <b>Время работы:</b> 24/7
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

def show_channel_link(message):
    """Показать ссылку на канал"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="about_service"))
    
    text = f"""
{EMOJI['channel']} <b>Наш канал</b>

{EMOJI['info']} <b>Подписывайтесь на наш канал для получения:</b>

{EMOJI['check']} Новостей о сервисе
{EMOJI['check']} Обновлений и улучшений
{EMOJI['check']} Полезных советов по VPN
{EMOJI['check']} Специальных предложений

{EMOJI['channel']} <b>Канал:</b> @yodevelop
"""
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['subs'])
def subs_command(message):
    """Обработчик команды /subs"""
    show_my_subscriptions(message)

@bot.message_handler(commands=['invite'])
def invite_command(message):
    """Обработчик команды /invite"""
    show_invite_menu(message)

if __name__ == "__main__":
    logger.info("Запуск бота...")
    
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
