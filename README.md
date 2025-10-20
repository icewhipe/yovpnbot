# 🤖 YoVPN Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-blue.svg)](https://core.telegram.org/bots/api)
[![Marzban](https://img.shields.io/badge/Marzban-API-green.svg)](https://github.com/Gozargah/Marzban)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Современный Telegram-бот для продажи VPN-подписок с ежедневной оплатой, асинхронной архитектурой и полной безопасностью данных.**

## ✨ Особенности

- 🔄 **Ежедневная оплата** — гибкая модель подписки (4 рубля в день)
- 🎨 **Современный UX/UI** — анимации, прогресс-бары, интуитивная навигация
- 🛡️ **Высокая безопасность** — защита от всех типов атак
- ⚡ **Асинхронная архитектура** — быстрый отклик и высокая производительность
- 📊 **Полный мониторинг** — Sentry, Prometheus, структурированные логи
- 🔧 **Готовность к продакшену** — Docker, CI/CD, автоматические тесты

## 🏗️ Структура проекта

```
yovpn-bot/
├── bot/                          # Основная логика бота (aiogram)
│   ├── handlers/                 # Обработчики команд и сообщений
│   │   ├── start_handler.py      # Команда /start
│   │   ├── subscription_handler.py # Управление подписками
│   │   ├── payment_handler.py    # Обработка платежей
│   │   ├── settings_handler.py   # Настройки пользователя
│   │   ├── support_handler.py    # Поддержка и FAQ
│   │   └── callback_handler.py   # Callback запросы
│   ├── middleware/               # Промежуточное ПО
│   │   ├── services_middleware.py # Сервисы в контексте
│   │   └── logging_middleware.py  # Логирование
│   ├── services/                 # Бизнес-логика
│   │   ├── user_service.py       # Управление пользователями
│   │   ├── marzban_service.py    # Интеграция с Marzban
│   │   ├── payment_service.py    # Обработка платежей
│   │   ├── notification_service.py # Уведомления
│   │   ├── animation_service.py  # Анимации и эффекты
│   │   └── ui_service.py         # Пользовательский интерфейс
│   └── main.py                   # Главный файл бота
├── src/                          # Дополнительные сервисы
│   ├── config/                   # Конфигурация
│   │   ├── config.py             # Основная конфигурация
│   │   └── monitoring.py         # Мониторинг
│   ├── services/                 # Дополнительные сервисы
│   ├── models/                   # Модели данных
│   └── utils/                    # Утилиты
├── assets/                       # Ресурсы
│   ├── emojis/                   # Эмодзи и интерфейс
│   │   └── interface.py          # Эмодзи для UI
│   └── animations/               # Анимации
│       └── effects.py            # Эффекты сообщений
├── tests/                        # Тесты
│   └── test_user_service.py      # Тесты сервисов
├── run_all.py                    # 🚀 Мастер-скрипт запуска
├── run.py                        # Простой скрипт запуска
├── check_config.py               # Проверка конфигурации
├── check_env.py                  # Проверка переменных окружения
├── requirements.txt              # Зависимости
├── requirements_async.txt        # Асинхронные зависимости
├── .env.sample                   # Пример конфигурации
├── docker-compose.yml            # Docker Compose
├── Dockerfile                    # Docker образ
└── README.md                     # Этот файл
```

## 🚀 Быстрый старт

### 1. Установка

```bash
# Клонируем репозиторий
git clone https://github.com/your-username/yovpn-bot.git
cd yovpn-bot

# Устанавливаем зависимости
pip install -r requirements.txt

# Настраиваем конфигурацию
cp .env.sample .env
nano .env
```

### 2. Настройка

Создайте файл `.env` с настройками:

```bash
# Telegram Bot Token
USERBOT_TOKEN=your_bot_token_here

# Marzban API
MARZBAN_API_URL=https://your-marzban-domain.com/api
MARZBAN_ADMIN_TOKEN=your_marzban_admin_token_here

# Дополнительные настройки
DAILY_COST=4.0
MIN_BALANCE_WARNING=8.0
LOG_LEVEL=INFO
```

### 3. Запуск

```bash
# 🚀 Рекомендуемый способ - мастер-скрипт
python3 run_all.py

# Или простой запуск
python3 run.py

# Или напрямую
python3 bot/main.py

# Или через Docker
docker-compose up -d
```

## 📋 Оставшиеся скрипты

После очистки репозитория остались только необходимые файлы:

### Основные скрипты:
- **`run_all.py`** - 🚀 Мастер-скрипт запуска (рекомендуется)
- **`run.py`** - Простой скрипт запуска
- **`bot/main.py`** - Основной файл бота (aiogram)

### Скрипты проверки:
- **`check_config.py`** - Проверка конфигурации
- **`check_env.py`** - Проверка переменных окружения

### Порядок выполнения:
1. `check_env.py` - проверяет переменные окружения
2. `check_config.py` - проверяет конфигурацию
3. `run_all.py` - запускает все проверки и бота

## 📱 Функции бота

### Основные команды

| Команда | Описание | UX особенность |
|---------|----------|----------------|
| `/start` | Главное меню | Анимированное приветствие с эффектом |
| `/help` | Справка | Интерактивная справка с примерами |
| `Мои подписки` | Управление подписками | Красивые карточки с QR-кодами |
| `Пополнить` | Пополнение баланса | Удобный выбор сумм и способов оплаты |

### Анимированные эффекты

Бот использует современные анимированные эффекты сообщений:

```python
# Примеры использования
await message.reply('Добро пожаловать!', message_effect_id='5044134455711629726')  # Сердечко
await message.reply('Платеж успешен!', message_effect_id='5046509860389126442')    # Хлопушка
await message.reply('Ошибка!', message_effect_id='5046589136895476101')             # Фекалия
```

**Доступные эффекты:**
- 🔥 Огонёк: `5104841245755180586`
- 👍 Палец вверх: `5107584321108051014`
- 👎 Палец вниз: `5104858069142078462`
- ❤️ Сердечко: `5044134455711629726`
- 🎉 Хлопушка: `5046509860389126442`
- 💩 Фекалия: `5046589136895476101`

### Современный UX/UI

- **Эмодзи-прогресс-бары:** `[███████░░░] 70%`
- **Анимированные уведомления:** Stickers + GIF + fallback emoji
- **QR-коды:** Для всех ссылок и конфигураций
- **Кнопки копирования:** One-click copy для всех данных
- **Немедленный отклик:** 0.1-0.3 секунды
- **Typing indicator:** Для всех долгих операций

## 🔧 Разработка

### Структура для разработчиков

#### Для джунов:
- **`bot/handlers/`** — здесь добавлять новые команды
- **`bot/services/`** — здесь бизнес-логика
- **`assets/emojis/interface.py`** — эмодзи для интерфейса
- **`assets/animations/effects.py`** — анимации сообщений

#### Для сеньоров:
- **`bot/middleware/`** — промежуточное ПО
- **`src/services/`** — дополнительные сервисы
- **`src/models/`** — модели данных
- **`src/utils/`** — вспомогательные функции

### Добавление новой команды

1. Создайте обработчик в `bot/handlers/`
2. Зарегистрируйте в `bot/handlers/__init__.py`
3. Добавьте кнопку в `bot/services/ui_service.py`
4. Обновите документацию

### Добавление нового сервиса

1. Создайте сервис в `bot/services/` или `src/services/`
2. Добавьте в соответствующий `__init__.py`
3. Инициализируйте в `bot/middleware/services_middleware.py`
4. Используйте в обработчиках

### Рекомендации для разработчиков

- **Всегда используйте `run_all.py`** для запуска - он проверяет конфигурацию
- **Добавляйте новые скрипты** только если они действительно нужны
- **Документируйте изменения** в README.md
- **Тестируйте** перед коммитом

## 🐳 Docker

### Запуск через Docker

```bash
# Сборка образа
docker build -t yovpn-bot .

# Запуск контейнера
docker run -d \
  --name yovpn-bot \
  --env-file .env \
  -p 8000:8000 \
  yovpn-bot

# Или с docker-compose
docker-compose up -d
```

### Docker Compose

```yaml
version: '3.8'
services:
  bot:
    build: .
    env_file: .env
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

## 📊 Мониторинг

### Prometheus метрики

```bash
# Просмотр метрик
curl http://localhost:8000/metrics
```

### Логирование

```bash
# Просмотр логов
tail -f bot.log

# Логи Docker
docker logs yovpn-bot
```

## 🛡️ Безопасность

### Проверка безопасности

```bash
# Статический анализ
bandit -r bot/

# Проверка зависимостей
safety check

# Аудит кода
semgrep --config=auto bot/
```

### Рекомендации

- Используйте переменные окружения для секретов
- Регулярно обновляйте зависимости
- Настройте мониторинг безопасности
- Используйте HTTPS для всех API

## 📈 Масштабирование

### Горизонтальное масштабирование

- **Load Balancer:** Распределение нагрузки
- **Database Sharding:** Разделение данных
- **CDN:** Кэширование статических ресурсов
- **Auto-scaling:** Автоматическое масштабирование

### Вертикальное масштабирование

- **Redis:** Кэширование и сессии
- **PostgreSQL:** Основная БД
- **Nginx:** Reverse proxy
- **Monitoring:** Полный мониторинг

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 📞 Поддержка

- **GitHub Issues:** [Создать issue](https://github.com/your-username/yovpn-bot/issues)
- **Telegram:** [@YoVPNSupport](https://t.me/YoVPNSupport)
- **Email:** support@yovpn.com

---

<div align="center">

**Сделано с ❤️ для безопасного интернета**

[![GitHub stars](https://img.shields.io/github/stars/your-username/yovpn-bot?style=social)](https://github.com/your-username/yovpn-bot)
[![Telegram](https://img.shields.io/badge/Telegram-@YoVPNBot-blue.svg)](https://t.me/YoVPNBot)

</div>