"""
Анимированные эффекты сообщений для Telegram
Все доступные эффекты с их ID и описанием
"""

# Анимированные эффекты сообщений Telegram
# ВАЖНО: ID эффектов могут изменяться Telegram. Если эффект не работает,
# бот автоматически отправит сообщение без эффекта.
MESSAGE_EFFECTS = {
    # Положительные эффекты
    'fire': {
        'id': '5104841245755180586',
        'name': 'Огонёк',
        'description': 'Анимированный огонь для успешных действий',
        'usage': 'Активация подписки, успешная оплата, достижения',
        'fallback_emoji': '🔥'
    },
    'thumbs_up': {
        'id': '5107584321108051014',
        'name': 'Палец вверх',
        'description': 'Одобрение и положительная оценка',
        'usage': 'Подтверждение действий, одобрение выбора',
        'fallback_emoji': '👍'
    },
    'heart': {
        'id': '5044134455711629726',
        'name': 'Сердечко',
        'description': 'Любовь и привязанность',
        'usage': 'Приветствие новых пользователей, благодарность',
        'fallback_emoji': '❤️'
    },
    'confetti': {
        'id': '5046509860389126442',
        'name': 'Хлопушка',
        'description': 'Празднование и радость',
        'usage': 'День рождения, юбилеи, особые достижения',
        'fallback_emoji': '🎉'
    },
    
    # Отрицательные эффекты
    'thumbs_down': {
        'id': '5104858069142078462',
        'name': 'Палец вниз',
        'description': 'Неодобрение и отрицательная оценка',
        'usage': 'Ошибки, отмена действий, предупреждения',
        'fallback_emoji': '👎'
    },
    'poop': {
        'id': '5046589136895476101',
        'name': 'Фекалия',
        'description': 'Неудача и разочарование',
        'usage': 'Критические ошибки, сбои системы',
        'fallback_emoji': '💩'
    },
    
    # Нейтральные эффекты
    'loading': {
        'id': '5104841245755180587',
        'name': 'Загрузка',
        'description': 'Процесс выполнения',
        'usage': 'Обработка запросов, настройка VPN',
        'fallback_emoji': '⏳'
    },
    'notification': {
        'id': '5104841245755180588',
        'name': 'Уведомление',
        'description': 'Информационное сообщение',
        'usage': 'Важные уведомления, обновления',
        'fallback_emoji': '🔔'
    }
}

def get_effect_id(effect_name: str) -> str:
    """
    Получить ID эффекта по имени
    
    Args:
        effect_name: Название эффекта (fire, thumbs_up, heart, etc.)
    
    Returns:
        str: ID эффекта для использования в message_effect_id
    """
    return MESSAGE_EFFECTS.get(effect_name, {}).get('id', '')

def get_effect_info(effect_name: str) -> dict:
    """
    Получить полную информацию об эффекте
    
    Args:
        effect_name: Название эффекта
    
    Returns:
        dict: Информация об эффекте
    """
    return MESSAGE_EFFECTS.get(effect_name, {})

def list_available_effects() -> list:
    """
    Получить список всех доступных эффектов
    
    Returns:
        list: Список названий эффектов
    """
    return list(MESSAGE_EFFECTS.keys())

# Примеры использования
USAGE_EXAMPLES = {
    'welcome': {
        'effect': 'heart',
        'message': 'Добро пожаловать в YoVPN! 💙',
        'description': 'Приветствие новых пользователей'
    },
    'subscription_activated': {
        'effect': 'fire',
        'message': '🎉 Подписка активирована! Наслаждайтесь безопасным интернетом!',
        'description': 'Успешная активация подписки'
    },
    'payment_success': {
        'effect': 'confetti',
        'message': '💰 Платеж успешно обработан! Баланс пополнен!',
        'description': 'Успешная оплата'
    },
    'error_critical': {
        'effect': 'poop',
        'message': '❌ Произошла критическая ошибка. Обратитесь в поддержку.',
        'description': 'Критические ошибки'
    },
    'loading_process': {
        'effect': 'loading',
        'message': '⏳ Настраиваю VPN-соединение...',
        'description': 'Процесс настройки'
    }
}

def get_usage_example(scenario: str) -> dict:
    """
    Получить пример использования для конкретного сценария
    
    Args:
        scenario: Сценарий использования (welcome, subscription_activated, etc.)
    
    Returns:
        dict: Пример использования с эффектом и сообщением
    """
    return USAGE_EXAMPLES.get(scenario, {})

# Функция для отправки сообщения с эффектом
async def send_message_with_effect(bot, chat_id: int, text: str, effect_name: str, **kwargs):
    """
    Отправить сообщение с анимированным эффектом
    
    Args:
        bot: Экземпляр бота
        chat_id: ID чата
        text: Текст сообщения
        effect_name: Название эффекта
        **kwargs: Дополнительные параметры для отправки сообщения
    
    Returns:
        Message: Отправленное сообщение
    """
    effect_id = get_effect_id(effect_name)
    
    if effect_id:
        kwargs['message_effect_id'] = effect_id
    
    return await bot.send_message(chat_id, text, **kwargs)

# Функция для ответа на сообщение с эффектом
async def reply_with_effect(bot, message, text: str, effect_name: str, **kwargs):
    """
    Ответить на сообщение с анимированным эффектом
    
    Args:
        bot: Экземпляр бота
        message: Сообщение для ответа
        text: Текст ответа
        effect_name: Название эффекта
        **kwargs: Дополнительные параметры
    
    Returns:
        Message: Отправленное сообщение
    """
    effect_id = get_effect_id(effect_name)
    
    if effect_id:
        kwargs['message_effect_id'] = effect_id
    
    return await message.reply(text, **kwargs)