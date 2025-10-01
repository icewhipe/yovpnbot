#!/usr/bin/env python3
"""
Telegram Bot для пользователей Marzban
"""

import os
import sys
import logging
import time
from decouple import config
import telebot
from telebot import types
from marzban_api import MarzbanAPI

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
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "Пользователь"
    
    # Если username None, используем first_name
    if not username:
        username = first_name.lower().replace(" ", "_")
    
    logger.info(f"Команда /start: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Проверяем, есть ли у пользователя подписка
    user_info = marzban_api.get_user_info(username) if username else None
    is_new_user = user_id not in test_users
    
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
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='HTML',
        reply_markup=keyboard
    )

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
    
    # Проверяем, есть ли у пользователя подписка
    user_info = marzban_api.get_user_info(username) if username else None
    is_new_user = user_id not in test_users
    
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

def get_test_period(message, username):
    """Получить тестовый период с анимацией"""
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
    
    # Создаем тестовый аккаунт
    logger.info(f"Создаем тестовый аккаунт для пользователя {username}")
    test_user = marzban_api.create_test_user(username, user_id)
    
    # Добавляем пользователя в список получивших тест
    test_users.add(user_id)
    
    if test_user:
        # Тестовый аккаунт создан - показываем успех
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['link']} Получить ссылку", callback_data=f"get_link_{username}"))
        
        success_text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['gift']} <b>🎉 Тестовый период активирован!</b>

{EMOJI['active']} <b>Статус:</b> Активен (тест)
{EMOJI['device']} <b>Устройства:</b> 0/3
{EMOJI['warning']} <b>Трафик:</b> 0 B / ∞
{EMOJI['info']} <b>Дней осталось:</b> 7

{EMOJI['rocket']} <b>Добро пожаловать!</b>
Вы получили 7 дней бесплатного доступа к VPN
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

{EMOJI['cross']} <b>Ошибка создания тестового аккаунта</b>

{EMOJI['rocket']} <b>Получите доступ к VPN:</b>
• Свободный интернет без ограничений
• Высокая скорость соединения
• Военная защита данных
• Подключение до 3 устройств
• Полная анонимность - никаких логов

{EMOJI['gift']} <b>Специальное предложение!</b>
Первый месяц всего за 109₽
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

def show_my_subscriptions(message):
    """Показать мои подписки"""
    keyboard = types.InlineKeyboardMarkup()
    
    # Получаем username из сообщения
    username = message.from_user.username
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Пользователь"
    
    logger.info(f"Пользователь: ID={user_id}, Username=@{username}, FirstName={first_name}")
    
    # Если username None, используем first_name
    if not username:
        username = first_name.lower().replace(" ", "_")
        logger.info(f"Username пустой, используем: {username}")
    
    logger.info(f"Ищем пользователя в Marzban: {username}")
    
    # Получаем данные пользователя из Marzban
    user_info = marzban_api.get_user_info(username)
    
    if not user_info:
        # Проверяем, новый ли это пользователь
        is_new_user = user_id not in test_users
        
        if is_new_user:
            # Новый пользователь - показываем кнопку тестового периода
            keyboard.add(
                types.InlineKeyboardButton(f"{EMOJI['gift']} Получить тестовый период", callback_data=f"get_test_{username}"),
                types.InlineKeyboardButton(f"{EMOJI['add']} Купить подписку", callback_data="add_subscription")
            )
            
            text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['gift']} <b>Добро пожаловать!</b>

{EMOJI['rocket']} <b>Получите 7 дней бесплатного доступа к VPN:</b>
• Свободный интернет без ограничений
• Высокая скорость соединения
• Военная защита данных
• Подключение до 3 устройств
• Полная анонимность - никаких логов

{EMOJI['gift']} <b>Нажмите "Получить тестовый период" и начните пользоваться VPN прямо сейчас!</b>
"""
        else:
            # Пользователь уже получал тест - показываем кнопку покупки
            keyboard.add(
                types.InlineKeyboardButton(f"{EMOJI['add']} Купить подписку", callback_data="add_subscription"),
                types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main")
            )
            
            text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['cross']} <b>У вас пока нет активной подписки</b>

{EMOJI['rocket']} <b>Получите доступ к VPN:</b>
• Свободный интернет без ограничений
• Высокая скорость соединения
• Военная защита данных
• Подключение до 3 устройств
• Полная анонимность - никаких логов

{EMOJI['gift']} <b>Специальное предложение!</b>
Первый месяц всего за 109₽
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
        
        # Добавляем кнопки для разных типов ссылок
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['link']} VLESS ссылки", callback_data=f"show_vless_{username}"))
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['subscription']} Подписка", callback_data=f"show_sub_{username}"))
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="my_subscriptions"))
        
        text = f"""
{EMOJI['link']} <b>Ссылки для установки VPN</b>

{EMOJI['rocket']} <b>Доступно:</b>
• VLESS ссылки: {len(links)} серверов
• Подписка: Готова к установке

{EMOJI['info']} <b>Выберите тип ссылки:</b>
• VLESS - для отдельных серверов
• Подписка - для автоматического обновления

{EMOJI['device']} <b>Поддерживаемые приложения:</b>
• v2rayNG, V2Box, Shadowrocket
• Clash, Sing-box, Outline
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
        keyboard.add(types.InlineKeyboardButton(f"{EMOJI['robot']} @yovpnrobot", url="https://t.me/yovpnrobot"))
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
• Clash, Sing-box, Outline
• v2rayNG (через подписку)
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
    
    text = f"""
{EMOJI['balance']} <b>Баланс:</b> 0 ₽

{EMOJI['info']} <b>Доступные действия:</b>

{EMOJI['payment']} <b>Пополнить баланс</b> - Добавить средства на счет
{EMOJI['history']} <b>История пополнения</b> - Посмотреть все транзакции
{EMOJI['coupon']} <b>Активировать купон</b> - Ввести промокод
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
    
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['share']} Поделиться ссылкой", url=f"https://t.me/share/url?url=https://t.me/{bot.get_me().username}?start=ref_{message.from_user.username}&text=Присоединяйся к лучшему VPN сервису!"),
        types.InlineKeyboardButton(f"{EMOJI['qr']} Показать QR-код", callback_data="show_qr"),
        types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main")
    )
    
    text = f"""
{EMOJI['referral']} <b>Реферальная система</b>

{EMOJI['info']} <b>Ваша статистика:</b>
• Приглашено: 0 человек
• Доход с рефералов: 0 ₽

{EMOJI['link']} <b>Ваша реферальная ссылка:</b>
https://t.me/{bot.get_me().username}?start=ref_{message.from_user.username}

{EMOJI['info']} <b>Уровни реферальной программы:</b>
• 1-й уровень: 25% от платежа
• 2-й уровень: 25% от платежа
• 3-й уровень: 10% от платежа
• 4-й уровень: 5% от платежа
• 5-й уровень: 2% от платежа
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
    
    text = f"""
{EMOJI['referral']} <b>Мои рефералы:</b>

{EMOJI['cross']} <b>Рефералов пока нет</b>

{EMOJI['info']} <b>Статистика:</b>
• Всего приглашено: 0
• Активных: 0
• Доход: 0 ₽

{EMOJI['link']} <b>Пригласите друзей и получайте доход!</b>
"""
    
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
• Windows, macOS, Linux
• iOS, Android
• Router, Smart TV

{EMOJI['security']} <b>Протоколы:</b>
• V2Ray, Clash, Sing-box
• Outline, Shadowsocks
• WireGuard, OpenVPN

{EMOJI['support']} <b>Техподдержка:</b>
Работаем круглосуточно для решения ваших вопросов
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

{EMOJI['warning']} <b>Платежная система не настроена</b>

{EMOJI['info']} <b>Для активации подписки обратитесь к администратору</b>

{EMOJI['support']} <b>Поддержка:</b> @your_support
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

{EMOJI['warning']} <b>Платежная система не настроена</b>

{EMOJI['info']} <b>Доступные способы оплаты:</b>
• Банковские карты
• Криптовалюты
• Электронные кошельки

{EMOJI['support']} <b>Для пополнения обратитесь к администратору</b>
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

{EMOJI['support']} <b>Техподдержка:</b> @your_support
{EMOJI['channel']} <b>Канал:</b> @your_channel
{EMOJI['info']} <b>Email:</b> support@yourdomain.com

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

{EMOJI['channel']} <b>Канал:</b> @your_channel
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
