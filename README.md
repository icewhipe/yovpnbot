# YOVPN Telegram Bot

Telegram-бот для управления VPN-подписками через Marzban API.

## 🚀 Возможности

- **Управление подписками**: Создание, продление и мониторинг VPN-подписок
- **Реферальная система**: Приглашение друзей с получением бонусов
- **Баланс и платежи**: Управление балансом пользователя
- **QR-коды**: Генерация QR-кодов для быстрого подключения
- **Мультиплатформенность**: Поддержка iOS, Android, Windows, macOS, AndroidTV

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- Marzban API доступ
- База данных (MySQL/PostgreSQL) - опционально

## 🛠 Установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd yovpn-telegram-bot
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте переменные окружения:**
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

4. **Запустите бота:**
```bash
python main_improved.py
```

## ⚙️ Конфигурация

Создайте файл `.env` на основе `.env.example`:

```env
# Telegram Bot Configuration
USERBOT_TOKEN=your_telegram_bot_token_here

# Marzban API Configuration
MARZBAN_API_URL=https://your-marzban-api-url.com/api
MARZBAN_ADMIN_TOKEN=your_marzban_admin_token_here

# Database Configuration (опционально)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=marzban
DB_USER=marzban
DB_PASSWORD=your_secure_database_password_here

# Data Storage
DATA_FILE=/workspace/data.json
```

## 🏗 Архитектура

Проект использует модульную архитектуру:

```
src/
├── config.py          # Конфигурация
├── models/
│   └── user.py        # Модель пользователя
├── services/
│   ├── user_service.py      # Сервис пользователей
│   └── marzban_service.py   # Сервис Marzban API
├── handlers/          # Обработчики команд
├── keyboards/         # Клавиатуры
└── utils/            # Утилиты
```

## 🔒 Безопасность

- ✅ SSL проверка включена для Marzban API
- ✅ Чувствительные данные в переменных окружения
- ✅ Валидация входных данных
- ✅ Обработка ошибок с логированием

## 🐳 Docker

Для запуска в Docker:

```bash
# Создайте docker-compose.yml
docker-compose up -d
```

## 📊 Мониторинг

Бот ведет подробные логи:
- Ошибки API запросов
- Действия пользователей
- Реферальные связи
- Системные события

## 🧪 Тестирование

```bash
# Запуск тестов
pytest tests/

# Покрытие кода
pytest --cov=src tests/
```

## 📝 API Документация

### Основные команды

- `/start` - Начало работы с ботом
- `/subs` - Просмотр подписок
- `/invite` - Реферальная система

### Callback данные

- `add_subscription` - Добавить подписку
- `my_subscriptions` - Мои подписки
- `balance` - Баланс
- `invite_friend` - Пригласить друга

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🆘 Поддержка

- **Telegram**: @icewhipe
- **Канал**: @yodevelop
- **Issues**: GitHub Issues

## 🔄 Changelog

### v2.0.0 (Текущая версия)
- ✅ Модульная архитектура
- ✅ Улучшенная безопасность
- ✅ Централизованная обработка ошибок
- ✅ Документация

### v1.0.0
- Базовая функциональность
- Интеграция с Marzban API
- Реферальная система