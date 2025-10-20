# 👨‍💻 Руководство разработчика YoVPN Bot

## 🎯 Обзор проекта

YoVPN Bot v2.0 — это полностью переработанный Telegram-бот для продажи VPN-подписок с современной архитектурой, красивым UX/UI и анимированными эффектами.

## 🏗️ Архитектура

### Структура папок

```
yovpn-bot/
├── bot/                          # 🎯 ОСНОВНАЯ ЛОГИКА БОТА
│   ├── handlers/                 # Обработчики команд и сообщений
│   ├── middleware/               # Промежуточное ПО
│   ├── services/                 # Бизнес-логика и сервисы
│   └── main.py                   # Главный файл бота
├── commands/                     # 📱 ОТДЕЛЬНЫЕ КОМАНДЫ
│   ├── user/                     # Пользовательские команды
│   ├── admin/                    # Административные команды
│   └── system/                   # Системные команды
├── utils/                        # 🛠️ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
│   ├── helpers/                  # Помощники
│   ├── validators/               # Валидаторы
│   └── formatters/               # Форматтеры
├── database/                     # 🗄️ БАЗА ДАННЫХ
│   ├── models/                   # Модели данных
│   └── migrations/               # Миграции
├── assets/                       # 🎨 РЕСУРСЫ
│   ├── emojis/                   # Эмодзи и интерфейс
│   ├── animations/               # Анимации
│   └── images/                   # Изображения
└── docs/                         # 📚 ДОКУМЕНТАЦИЯ
    ├── api/                      # API документация
    ├── guides/                   # Руководства
    └── examples/                 # Примеры
```

## 🚀 Быстрый старт для разработчиков

### 1. Настройка окружения

```bash
# Клонируем репозиторий
git clone https://github.com/your-username/yovpn-bot.git
cd yovpn-bot

# Создаем виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Настраиваем конфигурацию
cp .env.sample .env
nano .env  # Заполните настройки
```

### 2. Проверка конфигурации

```bash
# Проверяем настройки
python check_config.py

# Запускаем бота
python run.py
```

## 📁 Описание файлов

### 🎯 Основные файлы

| Файл | Назначение | Для кого |
|------|------------|----------|
| `bot/main.py` | Главный файл бота | Все |
| `run.py` | Скрипт запуска | Все |
| `check_config.py` | Проверка конфигурации | Все |
| `requirements.txt` | Зависимости | Все |

### 🤖 Обработчики команд (`bot/handlers/`)

| Файл | Назначение | Как редактировать |
|------|------------|-------------------|
| `start_handler.py` | Команда /start | Добавьте новые приветственные сообщения |
| `subscription_handler.py` | Управление подписками | Добавьте новые функции подписок |
| `payment_handler.py` | Обработка платежей | Добавьте новые способы оплаты |
| `settings_handler.py` | Настройки пользователя | Добавьте новые настройки |
| `support_handler.py` | Поддержка и FAQ | Обновите FAQ и контакты |
| `callback_handler.py` | Callback запросы | Добавьте новые callback обработчики |

### 🔧 Сервисы (`bot/services/`)

| Файл | Назначение | Как редактировать |
|------|------------|-------------------|
| `user_service.py` | Управление пользователями | Добавьте новые поля пользователя |
| `marzban_service.py` | Интеграция с Marzban | Добавьте новые API методы |
| `payment_service.py` | Обработка платежей | Добавьте новые платежные системы |
| `notification_service.py` | Уведомления | Добавьте новые типы уведомлений |
| `animation_service.py` | Анимации и эффекты | Добавьте новые эффекты |
| `ui_service.py` | Пользовательский интерфейс | Добавьте новые клавиатуры |

### 🎨 Ресурсы (`assets/`)

| Файл | Назначение | Как редактировать |
|------|------------|-------------------|
| `emojis/interface.py` | Эмодзи для UI | Добавьте новые эмодзи |
| `animations/effects.py` | Анимированные эффекты | Добавьте новые эффекты |

## 🎨 UX/UI рекомендации 2025-2026

### Современные тренды

1. **Микроанимации**
   - Используйте `message_effect_id` для важных сообщений
   - Добавляйте прогресс-бары для долгих операций
   - Создавайте плавные переходы между состояниями

2. **Персонализация**
   - Адаптируйте интерфейс под пользователя
   - Используйте имя пользователя в сообщениях
   - Предлагайте персонализированные рекомендации

3. **Геймификация**
   - Добавьте систему достижений
   - Создайте прогресс-бары для целей
   - Используйте эмодзи для визуальной обратной связи

### Примеры анимированных эффектов

```python
# Приветствие с сердечком
await message.reply('Добро пожаловать!', message_effect_id='5044134455711629726')

# Успешная оплата с хлопушкой
await message.reply('Платеж успешен!', message_effect_id='5046509860389126442')

# Ошибка с фекалией
await message.reply('Произошла ошибка!', message_effect_id='5046589136895476101')
```

## 🔧 Добавление новых функций

### 1. Новая команда

```python
# 1. Создайте обработчик в bot/handlers/
async def handle_new_command(callback: CallbackQuery):
    """Обработчик новой команды"""
    # Ваш код здесь
    pass

# 2. Зарегистрируйте в bot/handlers/__init__.py
dp.callback_query.register(handle_new_command, Text("new_command"))

# 3. Добавьте кнопку в bot/services/ui_service.py
def create_new_keyboard(self):
    keyboard = [
        [InlineKeyboardButton("Новая команда", callback_data="new_command")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
```

### 2. Новый сервис

```python
# 1. Создайте сервис в bot/services/
class NewService:
    def __init__(self):
        pass
    
    async def do_something(self):
        # Ваш код здесь
        pass

# 2. Добавьте в bot/services/__init__.py
from .new_service import NewService

# 3. Инициализируйте в bot/middleware/services_middleware.py
new_service = NewService()
services['new_service'] = new_service
```

### 3. Новый эффект анимации

```python
# 1. Добавьте в assets/animations/effects.py
MESSAGE_EFFECTS['new_effect'] = {
    'id': 'your_effect_id_here',
    'name': 'Новый эффект',
    'description': 'Описание эффекта',
    'usage': 'Когда использовать'
}

# 2. Используйте в коде
await message.reply('Сообщение', message_effect_id='your_effect_id_here')
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# Конкретный тест
pytest tests/test_specific.py

# С покрытием
pytest --cov=bot tests/
```

### Создание тестов

```python
# tests/test_new_feature.py
import pytest
from bot.services.new_service import NewService

@pytest.mark.asyncio
async def test_new_feature():
    service = NewService()
    result = await service.do_something()
    assert result is not None
```

## 🐳 Docker

### Разработка

```bash
# Сборка образа
docker build -t yovpn-bot .

# Запуск контейнера
docker run -d --name yovpn-bot --env-file .env yovpn-bot

# Просмотр логов
docker logs yovpn-bot
```

### Продакшен

```bash
# Запуск через docker-compose
docker-compose up -d

# Остановка
docker-compose down

# Обновление
docker-compose pull
docker-compose up -d
```

## 📊 Мониторинг

### Prometheus метрики

```bash
# Просмотр метрик
curl http://localhost:8000/metrics
```

### Grafana дашборды

```bash
# Откройте в браузере
http://localhost:3000
# Логин: admin, Пароль: admin
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
- Валидируйте все входные данные
- Логируйте все важные события
- Регулярно обновляйте зависимости

## 🚀 Развертывание

### VPS

```bash
# Установка зависимостей
sudo apt update
sudo apt install python3-pip docker.io docker-compose

# Клонирование репозитория
git clone https://github.com/your-username/yovpn-bot.git
cd yovpn-bot

# Настройка
cp .env.sample .env
nano .env

# Запуск
docker-compose up -d
```

### Облако

- **AWS:** Используйте ECS или EC2
- **Google Cloud:** Используйте Cloud Run или GKE
- **Azure:** Используйте Container Instances или AKS

## 📚 Полезные ресурсы

- [aiogram документация](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Marzban документация](https://github.com/Gozargah/Marzban)
- [Docker документация](https://docs.docker.com/)

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📞 Поддержка

- **GitHub Issues:** [Создать issue](https://github.com/your-username/yovpn-bot/issues)
- **Telegram:** [@YoVPNSupport](https://t.me/YoVPNSupport)
- **Email:** support@yovpn.com

---

**Удачной разработки! 🚀**