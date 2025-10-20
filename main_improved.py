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
from src.services.daily_payment_service import DailyPaymentService
from src.services.notification_service import NotificationService
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
notification_service = NotificationService()

# Создание бота
bot = telebot.TeleBot(config.BOT_TOKEN)

# Устанавливаем бота в сервис уведомлений
notification_service.set_bot(bot)

# Создание сервиса ежедневной оплаты
daily_payment_service = DailyPaymentService(marzban_service, user_service)

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
    
    # Приветственный бонус 20 ₽ (однократно) - 5 дней доступа
    if not user.bonus_given:
        user_service.add_balance(user_id, 20)
        user_service.update_user_record(user_id, {"bonus_given": True})
        
        # Отправляем уведомление о приветственном бонусе
        notification_service.send_welcome_bonus_notification(user_id, 20, 20)
    
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
    
    # Если пользователь не найден в Marzban, создаем его
    if not user_info and username:
        logger.info(f"Пользователь {username} не найден в Marzban, создаем...")
        try:
            # Получаем баланс пользователя
            user_stats = user_service.get_user_stats(user_id)
            balance = user_stats.get('balance', 0)
            
            if balance >= 4:  # Если есть средства на 1 день
                # Создаем пользователя с подпиской на 1 день
                created_user = marzban_service.create_user(username, user_id, days=1)
                if created_user:
                    logger.info(f"Пользователь {username} успешно создан в Marzban с подпиской на 1 день")
                    # Получаем информацию о созданном пользователе
                    user_info = marzban_service.get_user_info(username)
                else:
                    logger.warning(f"Не удалось создать пользователя {username} в Marzban")
            else:
                logger.info(f"Недостаточно средств для создания подписки у пользователя {username}")
        except Exception as e:
            logger.error(f"Ошибка создания пользователя {username}: {e}")
    
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
    balance = user_stats.get('balance', 0)
    days = user_stats.get('days_remaining', 0)
    
    # Проверяем статус подписки
    subscription_status = "Активна" if user_info and user_info.get('status') == 'active' else "Неактивна"
    subscription_emoji = "🟢" if user_info and user_info.get('status') == 'active' else "🔴"
    
    if user_info:
        # Пользователь с подпиской
        welcome_text = f"""
{EMOJI['user']} <b>Добро пожаловать, {first_name}!</b>

<b>Ваш профиль:</b>
├ ID: {user_id}
├ Username: @{username}
├ Баланс: {balance} ₽ (≈ {days} дн.)
├ Подписка: {subscription_emoji} {subscription_status}
└ Стоимость: 4 ₽/день

{EMOJI['rocket']} <b>Выберите действие:</b>
"""
    elif is_new_user:
        # Новый пользователь
        welcome_text = f"""
{EMOJI['user']} <b>Добро пожаловать, {first_name}!</b>

{EMOJI['gift']} <b>Подарок для новых пользователей!</b>
Вы получили 20 ₽ на баланс (5 дней доступа)

<b>Ваш профиль:</b>
├ ID: {user_id}
├ Username: @{username}
├ Баланс: {balance} ₽ (≈ {days} дн.)
├ Подписка: 🔴 Неактивна
└ Стоимость: 4 ₽/день

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

@handle_error
def show_my_subscriptions(message):
    """Показать подписки пользователя"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "user"
    
    # Получаем информацию о пользователе из Marzban
    user_info = marzban_service.get_user_info(username)
    
    # Получаем статистику пользователя
    user_stats = user_service.get_user_stats(user_id)
    balance = user_stats.get('balance', 0)
    days_remaining = user_stats.get('days_remaining', 0)
    
    if not user_info:
        text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{EMOJI['warning']} <b>У вас нет активных подписок</b>

<b>Ваш баланс:</b> {balance} ₽
<b>Доступно дней:</b> {days_remaining}
<b>Стоимость:</b> 4 ₽/день

Для активации подписки пополните баланс.
"""
    else:
        # Формируем информацию о подписке
        status = user_info.get('status', 'Неизвестно')
        status_emoji = "🟢" if status == 'active' else "🔴"
        
        text = f"""
{EMOJI['subscription']} <b>Мои подписки</b>

{status_emoji} <b>Статус:</b> {status}
{EMOJI['balance']} <b>Баланс:</b> {balance} ₽
{EMOJI['calendar']} <b>Доступно дней:</b> {days_remaining}
{EMOJI['device']} <b>Трафик:</b> Безлимит
{EMOJI['money']} <b>Стоимость:</b> 4 ₽/день

{EMOJI['info']} Подписка продлевается автоматически при наличии средств на балансе.
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_invite_menu(message):
    """Показать меню приглашения друзей"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "user"
    
    # Получаем статистику рефералов
    user_stats = user_service.get_user_stats(user_id)
    referrals_count = user_stats.get('referrals_count', 0)
    referral_income = user_stats.get('referral_income', 0)
    
    # Создаем реферальную ссылку
    bot_username = bot.get_me().username
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    text = f"""
{EMOJI['referral']} <b>Пригласите друзей и получайте бонусы!</b>

{EMOJI['info']} <b>Как это работает:</b>
• Отправьте другу вашу реферальную ссылку
• Друг переходит по ссылке и регистрируется
• Вы получаете 12 ₽ на баланс
• Друг получает 20 ₽ приветственный бонус

{EMOJI['link']} <b>Ваша реферальная ссылка:</b>
<code>{referral_link}</code>

{EMOJI['info']} <b>Ваша статистика:</b>
• Приглашено друзей: {referrals_count}
• Заработано с рефералов: {referral_income} ₽
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton(f"{EMOJI['share']} Поделиться", callback_data="share_link"),
        types.InlineKeyboardButton(f"{EMOJI['qr']} QR-код", callback_data="show_qr")
    )
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_referrals_menu(message):
    """Показать меню рефералов"""
    user_id = message.from_user.id
    user_stats = user_service.get_user_stats(user_id)
    referrals_count = user_stats.get('referrals_count', 0)
    referral_income = user_stats.get('referral_income', 0)
    
    text = f"""
{EMOJI['referral']} <b>Мои рефералы</b>

{EMOJI['info']} <b>Статистика:</b>
• Приглашено друзей: {referrals_count}
• Заработано с рефералов: {referral_income} ₽

{EMOJI['info']} <b>Как приглашать:</b>
1. Поделитесь реферальной ссылкой
2. Друг переходит по ссылке
3. Вы получаете 12 ₽ бонус
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_about_service(message):
    """Показать информацию о сервисе"""
    text = f"""
{EMOJI['info']} <b>О сервисе YoVPN</b>

{EMOJI['speed']} <b>Высокая скорость</b>
Серверы в 50+ странах мира

{EMOJI['security']} <b>Безопасность</b>
Военный уровень шифрования

{EMOJI['no_logs']} <b>Без логов</b>
Мы не храним ваши данные

{EMOJI['active']} <b>Стабильность</b>
Работаем 24/7 без перебоев

{EMOJI['device']} <b>Устройства</b>
До 3 устройств одновременно

{EMOJI['support']} <b>Поддержка</b>
Круглосуточная помощь
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_payment_options(message):
    """Показать варианты пополнения"""
    text = f"""
{EMOJI['payment']} <b>Пополнение баланса</b>

{EMOJI['info']} <b>Доступные способы:</b>
• Банковская карта
• СБП (Система быстрых платежей)
• Криптовалюта
• Электронные кошельки

{EMOJI['warning']} <b>Внимание:</b> Функция в разработке
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="balance"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_payment_history(message):
    """Показать историю платежей"""
    text = f"""
{EMOJI['history']} <b>История платежей</b>

{EMOJI['warning']} <b>Внимание:</b> Функция в разработке
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="balance"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def activate_coupon(message):
    """Активация купона"""
    text = f"""
{EMOJI['coupon']} <b>Активация купона</b>

{EMOJI['warning']} <b>Внимание:</b> Функция в разработке
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="balance"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def share_referral_link(message):
    """Поделиться реферальной ссылкой"""
    user_id = message.from_user.id
    bot_username = bot.get_me().username
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    text = f"""
{EMOJI['share']} <b>Поделиться реферальной ссылкой</b>

{EMOJI['link']} <b>Ваша ссылка:</b>
<code>{referral_link}</code>

{EMOJI['info']} <b>Как поделиться:</b>
1. Скопируйте ссылку выше
2. Отправьте другу в любом мессенджере
3. Друг переходит по ссылке
4. Вы получаете 12 ₽ бонус
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="invite_friend"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_qr_code(message):
    """Показать QR-код реферальной ссылки"""
    user_id = message.from_user.id
    bot_username = bot.get_me().username
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    if QR_AVAILABLE:
        try:
            # Генерируем QR-код
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(referral_link)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Конвертируем в BytesIO
            bio = BytesIO()
            img.save(bio, 'PNG')
            bio.seek(0)
            
            # Отправляем QR-код
            bot.send_photo(
                message.chat.id,
                photo=bio,
                caption=f"{EMOJI['qr']} <b>QR-код реферальной ссылки</b>\n\n{EMOJI['info']} Поделитесь этим QR-кодом с друзьями!",
                parse_mode='HTML'
            )
            return
        except Exception as e:
            logger.warning(f"Ошибка генерации QR-кода: {e}")
    
    # Если QR-код не удалось сгенерировать, показываем ссылку
    text = f"""
{EMOJI['qr']} <b>QR-код реферальной ссылки</b>

{EMOJI['link']} <b>Ваша ссылка:</b>
<code>{referral_link}</code>

{EMOJI['info']} <b>Как использовать:</b>
1. Поделитесь QR-кодом с друзьями
2. Друг сканирует QR-код
3. Вы получаете 12 ₽ бонус
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="invite_friend"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_support_chat(message):
    """Показать контакты поддержки"""
    text = f"""
{EMOJI['support']} <b>Поддержка</b>

{EMOJI['info']} <b>Способы связи:</b>
• Telegram: @yovpn_support
• Email: support@yovpn.com
• Время работы: 24/7

{EMOJI['warning']} <b>Внимание:</b> Функция в разработке
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

@handle_error
def show_channel_link(message):
    """Показать ссылку на канал"""
    text = f"""
{EMOJI['channel']} <b>Наш канал</b>

{EMOJI['info']} <b>Подписывайтесь на наш канал:</b>
• Новости и обновления
• Полезные советы
• Специальные предложения

{EMOJI['warning']} <b>Внимание:</b> Функция в разработке
"""
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        message.chat.id,
        message.message_id,
        parse_mode='HTML',
        reply_markup=keyboard
    )

# Заглушки для остальных функций
@handle_error
def get_test_period(message, username):
    """Получить тестовый период"""
    user_id = message.from_user.id
    
    # Получаем статистику пользователя
    user_stats = user_service.get_user_stats(user_id)
    balance = user_stats.get('balance', 0)
    
    if balance >= 4:  # Если есть средства на 1 день
        # Создаем пользователя в Marzban с подпиской на 1 день
        try:
            created_user = marzban_service.create_user(username, user_id, days=1)
            if created_user:
                text = f"""
{EMOJI['gift']} <b>Подписка активирована!</b>

{EMOJI['check']} Ваша подписка успешно создана
{EMOJI['balance']} Баланс: {balance} ₽
{EMOJI['calendar']} Доступно дней: {int(balance / 4)}
{EMOJI['money']} Стоимость: 4 ₽/день

{EMOJI['info']} Подписка будет продлеваться автоматически при наличии средств на балансе.
"""
                bot.send_message(message.chat.id, text, parse_mode='HTML')
                
                # Отправляем уведомление о возобновлении подписки
                notification_service.send_subscription_reactivated_notification(user_id, balance)
            else:
                bot.send_message(message.chat.id, f"{EMOJI['error']} <b>Ошибка активации</b>\n\nНе удалось создать подписку. Попробуйте позже.")
        except Exception as e:
            logger.error(f"Ошибка создания подписки для {username}: {e}")
            bot.send_message(message.chat.id, f"{EMOJI['error']} <b>Ошибка активации</b>\n\nПроизошла ошибка при создании подписки.")
    else:
        text = f"""
{EMOJI['warning']} <b>Недостаточно средств</b>

{EMOJI['balance']} Ваш баланс: {balance} ₽
{EMOJI['money']} Требуется: 4 ₽ (1 день)

Пополните баланс для активации подписки.
"""
        bot.send_message(message.chat.id, text, parse_mode='HTML')

@handle_error
def handle_subscription_purchase(message, callback_data):
    """Обработка покупки подписки"""
    bot.send_message(message.chat.id, f"{EMOJI['subscription']} <b>Покупка подписки</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def show_setup_step1(message):
    """Показать первый шаг настройки"""
    bot.send_message(message.chat.id, f"{EMOJI['settings']} <b>Настройка VPN</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def show_setup_step2(message, device_key):
    """Показать второй шаг настройки"""
    bot.send_message(message.chat.id, f"{EMOJI['settings']} <b>Настройка VPN</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def continue_setup_flow(message):
    """Продолжить настройку"""
    bot.send_message(message.chat.id, f"{EMOJI['settings']} <b>Настройка VPN</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def finish_setup(message):
    """Завершить настройку"""
    bot.send_message(message.chat.id, f"{EMOJI['settings']} <b>Настройка VPN</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def show_qr_key(message):
    """Показать QR-код ключа"""
    bot.send_message(message.chat.id, f"{EMOJI['qr']} <b>QR-код ключа</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def show_vpn_links(message, username):
    """Показать VPN ссылки"""
    bot.send_message(message.chat.id, f"{EMOJI['vpn']} <b>VPN ссылки</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def show_vless_links(message, username):
    """Показать VLESS ссылки"""
    bot.send_message(message.chat.id, f"{EMOJI['vpn']} <b>VLESS ссылки</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def show_subscription_link(message, username):
    """Показать ссылку подписки"""
    bot.send_message(message.chat.id, f"{EMOJI['subscription']} <b>Ссылка подписки</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def copy_vless_link(message, callback_data):
    """Скопировать VLESS ссылку"""
    bot.send_message(message.chat.id, f"{EMOJI['vpn']} <b>Копирование ссылки</b>\n\n{EMOJI['warning']} Функция в разработке")

@handle_error
def get_vless_configs(message, username):
    """Получить VLESS конфигурации"""
    bot.send_message(message.chat.id, f"{EMOJI['vpn']} <b>VLESS конфигурации</b>\n\n{EMOJI['warning']} Функция в разработке")

if __name__ == "__main__":
    logger.info("Запуск улучшенного бота...")
    
    # Проверяем доступность Marzban API
    if not marzban_service.health_check():
        logger.warning("Marzban API недоступен, но бот продолжает работу")
    
    # Запускаем систему ежедневной оплаты
    try:
        daily_payment_service.start_daily_checker()
        logger.info("Система ежедневной оплаты запущена")
    except Exception as e:
        logger.error(f"Ошибка запуска системы ежедневной оплаты: {e}")
    
    # Проверяем пользователей с низким балансом
    try:
        daily_payment_service.check_low_balance_users()
        logger.info("Проверка пользователей с низким балансом завершена")
    except Exception as e:
        logger.error(f"Ошибка проверки пользователей с низким балансом: {e}")
    
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