# 💎 YoVPN Bot - Telegram VPN бот с админ-панелью

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![aiogram](https://img.shields.io/badge/aiogram-3.4+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Современный Telegram бот для продажи VPN подписок с интеграцией Marzban**

**🆕 Расширенная версия с текстовым режимом и 5-уровневой реферальной системой**

[Возможности](#-возможности) • [Установка](#-установка) • [Деплой](#-деплой) • [Документация](#-документация) • [Поддержка](#-поддержка)

</div>

---

## 🆕 Новые функции (v2.0)

### 🤖 Текстовый режим
- ✅ Анимированный `/start` с приветственным бонусом
- ✅ Проверка подписки на канал @yodevelop
- ✅ 3-шаговая активация VPN
- ✅ Автоматическая интеграция с Marzban

### 👥 Реферальная система (5 уровней)
- ✅ **1 день VPN** за каждого приглашенного друга
- ✅ **До 10%** от пополнений рефералов всех уровней
- ✅ Автоматическое начисление бонусов
- ✅ Детальная статистика по уровням

### ⚙️ Расширенная админ-панель
- ✅ **Статистика** (общая, пользователи, финансы, Marzban)
- ✅ **Управление балансом** (пополнить, списать, установить)
- ✅ **Настройки Marzban** (тест, синхронизация)
- ✅ **Безопасность** (логи, мониторинг, бэкапы)

📖 Подробнее: [README_EXTENDED.md](README_EXTENDED.md) | [ЧТО_РЕАЛИЗОВАНО.md](ЧТО_РЕАЛИЗОВАНО.md)

---

## 📋 Содержание

- [Возможности](#-возможности)
- [Архитектура](#-архитектура)
- [Требования](#-требования)
- [Быстрый старт](#-быстрый-старт)
- [Установка](#-установка)
- [Конфигурация](#-конфигурация)
- [Деплой](#-деплой)
  - [Railway](#railway)
  - [VPS Ubuntu](#vps-ubuntu-2404)
  - [Docker](#docker)
- [Использование](#-использование)
- [API Документация](#-api-документация)
- [Разработка](#-разработка)
- [Поддержка](#-поддержка)
- [Лицензия](#-лицензия)

---

## ✨ Возможности

### 🤖 Telegram Бот
- ✅ **Два режима работы**: WebApp (современный UI) и текстовый режим
- 💎 **Приветственный бонус**: 3 дня бесплатного доступа (12 руб)
- 📱 **Анимированный интерфейс** с плавными переходами
- 🎁 **Реферальная система** с бонусами
- 💳 **Ежедневная модель оплаты** (4 рубля в день)
- 🔐 **Автоматическая активация** VPN через Marzban API
- 📊 **Статистика использования** трафика и времени
- 💬 **Поддержка пользователей** через Telegram

### ⚙️ Админ-панель
- 🎛️ **Web-интерфейс** на FastAPI + Jinja2 + Tailwind CSS
- 👥 **Управление пользователями** (блокировка, баланс, статистика)
- 🛰️ **Управление подписками** (активация, деактивация, продление)
- 📡 **Рассылки** с фото и кнопками
- 🔧 **Настройки бота** (цены, бонусы, режимы)
- 📈 **Дашборд** с реальной статистикой
- 🔄 **Переключение режимов** (WebApp/Текстовый, Техобслуживание)

### 🌐 Marzban Integration
- ✅ **Полная интеграция** с Marzban API
- 🔄 **Автоматическое создание** подписок
- 📊 **Синхронизация данных** с Marzban
- 🗄️ **Общая база данных** MySQL с Marzban
- 🔐 **Безопасное хранение** токенов и ключей

---

## 🏗️ Архитектура

```
/workspace
├── bot/                    # Telegram бот (aiogram 3.x)
│   ├── handlers/          # Обработчики команд и событий
│   ├── keyboards/         # Клавиатуры и кнопки
│   ├── middleware/        # Middleware для бота
│   ├── services/          # Бизнес-логика
│   ├── utils/             # Вспомогательные функции
│   └── main.py            # Точка входа бота
│
├── admin/                  # Админ-панель (FastAPI)
│   ├── routes/            # API роуты
│   ├── templates/         # HTML шаблоны (Jinja2)
│   ├── static/            # Статические файлы (CSS, JS, изображения)
│   └── main.py            # Точка входа админки
│
├── api/                    # API клиенты
│   └── marzban_api.py     # Клиент для Marzban API
│
├── database/               # База данных
│   ├── models.py          # SQLAlchemy модели
│   ├── db.py              # Подключение к БД
│   └── migrations/        # Alembic миграции
│
├── config/                 # Конфигурация
│   └── settings.py        # Настройки из .env
│
├── utils/                  # Утилиты
│   ├── logger.py          # Логирование
│   └── helpers.py         # Вспомогательные функции
│
├── .env.example            # Пример конфигурации
├── requirements.txt        # Python зависимости
├── alembic.ini            # Конфигурация Alembic
├── docker-compose.yml     # Docker Compose
└── Dockerfile             # Docker образ
```

---

## 📦 Требования

### Минимальные требования
- Python 3.11+
- MySQL 8.0+
- Redis 7.0+ (опционально, для кэширования)
- Marzban установленный и настроенный

### Для разработки
- Docker и Docker Compose (опционально)
- Git

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/yovpn-bot.git
cd yovpn-bot
```

### 2. Создание виртуального окружения

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Конфигурация

```bash
cp .env.example .env
nano .env  # Отредактируйте настройки
```

**Минимальная конфигурация:**
```env
BOT_TOKEN=your_bot_token_here
ADMIN_TG_ID=7610842643
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/yovpn
MARZBAN_API_URL=http://localhost:8000
MARZBAN_API_TOKEN=your_marzban_token
```

### 5. Инициализация базы данных

```bash
# Создайте базу данных MySQL
mysql -u root -p -e "CREATE DATABASE yovpn CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Примените миграции
alembic upgrade head
```

### 6. Запуск

```bash
# Запуск бота
python bot/main.py

# Запуск админ-панели (в отдельном терминале)
uvicorn admin.main:app --host 0.0.0.0 --port 8080 --reload
```

🎉 **Готово!** Бот запущен и готов к работе.

---

## 🔧 Конфигурация

### Основные настройки (.env)

| Переменная | Описание | Значение по умолчанию |
|-----------|----------|----------------------|
| `BOT_TOKEN` | Токен Telegram бота | - |
| `ADMIN_TG_ID` | Telegram ID администратора | `7610842643` |
| `DATABASE_URL` | URL базы данных MySQL | `mysql+aiomysql://...` |
| `MARZBAN_API_URL` | URL Marzban API | `http://localhost:8000` |
| `MARZBAN_API_TOKEN` | Токен Marzban API | - |
| `ADMIN_PORT` | Порт админ-панели | `8080` |
| `DAILY_PRICE` | Цена за день (руб) | `4.0` |
| `WELCOME_BONUS` | Приветственный бонус (руб) | `12.0` |
| `REFERRAL_BONUS` | Реферальный бонус (руб) | `8.0` |

### Настройки через админ-панель

После запуска админ-панели перейдите по адресу `http://localhost:8080/admin/settings`:

- 🛠️ **Режим техобслуживания** - приостановить работу бота
- 🌐 **WebApp режим** - переключение между WebApp и текстовым режимом
- 💰 **Цены и бонусы** - настройка экономики
- 💬 **Контакты поддержки** - username поддержки и канала

---

## 🌍 Деплой

### Railway

Railway - простой и быстрый способ деплоя с автоматическим масштабированием.

#### Шаг 1: Подготовка

1. Создайте аккаунт на [Railway.app](https://railway.app)
2. Установите Railway CLI:
```bash
npm install -g @railway/cli
railway login
```

#### Шаг 2: Создание проекта

```bash
# Инициализация проекта
railway init

# Создание MySQL сервиса
railway add mysql

# Создание Redis сервиса (опционально)
railway add redis
```

#### Шаг 3: Настройка переменных окружения

```bash
# Устанавливаем переменные
railway variables set BOT_TOKEN=your_bot_token
railway variables set ADMIN_TG_ID=7610842643
railway variables set MARZBAN_API_URL=http://your-marzban-url
railway variables set MARZBAN_API_TOKEN=your_token
```

Или через Railway Dashboard: Project → Variables

#### Шаг 4: Деплой

```bash
# Деплой бота
railway up

# Применение миграций
railway run alembic upgrade head
```

#### Шаг 5: Мониторинг

```bash
# Просмотр логов
railway logs

# Статус сервисов
railway status
```

**💡 Совет:** Railway автоматически устанавливает `DATABASE_URL` при подключении MySQL.

---

### VPS Ubuntu 24.04

Детальная инструкция для деплоя на чистый VPS.

#### Требования сервера

- **ОС**: Ubuntu 24.04 LTS
- **CPU**: 1 vCPU (минимум)
- **RAM**: 2 GB (минимум)
- **Диск**: 20 GB NVMe
- **Сеть**: 100 Mbps+

#### Шаг 1: Подключение к серверу

```bash
ssh root@your-server-ip
```

#### Шаг 2: Обновление системы

```bash
apt update && apt upgrade -y
```

#### Шаг 3: Установка зависимостей

```bash
# Python 3.11
apt install -y python3.11 python3.11-venv python3-pip

# MySQL
apt install -y mysql-server mysql-client libmysqlclient-dev

# Redis (опционально)
apt install -y redis-server

# Nginx
apt install -y nginx

# Git
apt install -y git

# Дополнительные пакеты
apt install -y build-essential pkg-config
```

#### Шаг 4: Настройка MySQL

```bash
# Безопасная установка MySQL
mysql_secure_installation

# Создание базы данных и пользователя
mysql -u root -p << EOF
CREATE DATABASE yovpn CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'yovpn'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON yovpn.* TO 'yovpn'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF
```

#### Шаг 5: Создание пользователя для приложения

```bash
# Создаем пользователя
useradd -m -s /bin/bash yovpn
usermod -aG sudo yovpn

# Переключаемся на пользователя
su - yovpn
```

#### Шаг 6: Клонирование и настройка

```bash
# Клонируем репозиторий
git clone https://github.com/yourusername/yovpn-bot.git
cd yovpn-bot

# Создаем виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Настраиваем .env
cp .env.example .env
nano .env
```

**Настройте .env:**
```env
BOT_TOKEN=your_bot_token
ADMIN_TG_ID=7610842643
DATABASE_URL=mysql+aiomysql://yovpn:strong_password_here@localhost:3306/yovpn
MARZBAN_API_URL=http://localhost:8000
MARZBAN_API_TOKEN=your_token
ADMIN_PORT=8080
```

#### Шаг 7: Применение миграций

```bash
alembic upgrade head
```

#### Шаг 8: Настройка Systemd Services

**Бот сервис** (`/etc/systemd/system/yovpn-bot.service`):

```ini
[Unit]
Description=YoVPN Telegram Bot
After=network.target mysql.service

[Service]
Type=simple
User=yovpn
WorkingDirectory=/home/yovpn/yovpn-bot
Environment="PATH=/home/yovpn/yovpn-bot/venv/bin"
ExecStart=/home/yovpn/yovpn-bot/venv/bin/python bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Админ-панель сервис** (`/etc/systemd/system/yovpn-admin.service`):

```ini
[Unit]
Description=YoVPN Admin Panel
After=network.target mysql.service

[Service]
Type=simple
User=yovpn
WorkingDirectory=/home/yovpn/yovpn-bot
Environment="PATH=/home/yovpn/yovpn-bot/venv/bin"
ExecStart=/home/yovpn/yovpn-bot/venv/bin/uvicorn admin.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Шаг 9: Запуск сервисов

```bash
# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable yovpn-bot
sudo systemctl enable yovpn-admin

# Запускаем
sudo systemctl start yovpn-bot
sudo systemctl start yovpn-admin

# Проверяем статус
sudo systemctl status yovpn-bot
sudo systemctl status yovpn-admin
```

#### Шаг 10: Настройка Nginx (опционально)

**Конфигурация** (`/etc/nginx/sites-available/yovpn-admin`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Активируем конфигурацию
sudo ln -s /etc/nginx/sites-available/yovpn-admin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### Шаг 11: SSL сертификат (рекомендуется)

```bash
# Установка Certbot
sudo apt install -y certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d your-domain.com
```

#### Шаг 12: Мониторинг

```bash
# Логи бота
sudo journalctl -u yovpn-bot -f

# Логи админки
sudo journalctl -u yovpn-admin -f

# Статус всех сервисов
sudo systemctl status yovpn-*
```

---

### Docker

Самый простой способ запуска через Docker Compose.

#### Шаг 1: Установка Docker

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo apt install -y docker-compose
```

#### Шаг 2: Настройка

```bash
# Клонируем репозиторий
git clone https://github.com/yourusername/yovpn-bot.git
cd yovpn-bot

# Настраиваем .env
cp .env.example .env
nano .env
```

#### Шаг 3: Запуск

```bash
# Сборка и запуск всех сервисов
docker-compose up -d

# Применение миграций
docker-compose run --rm migrations

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

#### Управление

```bash
# Перезапуск бота
docker-compose restart bot

# Перезапуск админки
docker-compose restart admin

# Просмотр статуса
docker-compose ps

# Обновление
git pull
docker-compose build
docker-compose up -d
```

---

## 📚 Использование

### Для пользователей

1. **Запуск бота**: Найдите бота в Telegram и нажмите `/start`
2. **Получение бонуса**: При первом запуске получите 3 дня бесплатно (12 руб)
3. **Активация VPN**: 
   - Выберите устройство (iOS, Android, Windows, Mac, Linux)
   - Скачайте рекомендуемое приложение
   - Получите конфигурацию и активируйте
4. **Пополнение**: Пополните баланс через встроенные методы оплаты
5. **Реферальная программа**: Приглашайте друзей и получайте бонусы

### Для администратора

1. **Доступ к админке**: `http://your-server:8080/admin`
2. **Управление пользователями**: 
   - Просмотр всех пользователей
   - Блокировка/разблокировка
   - Изменение баланса
   - Просмотр транзакций
3. **Управление подписками**:
   - Просмотр активных подписок
   - Деактивация/активация
   - Синхронизация с Marzban
4. **Рассылки**:
   - Создание рассылки с текстом
   - Добавление изображений
   - Кнопки с ссылками
5. **Настройки**:
   - Переключение режимов
   - Изменение цен и бонусов
   - Настройка контактов поддержки

---

## 📖 API Документация

После запуска админ-панели доступна автоматическая документация:

- **Swagger UI**: `http://your-server:8080/admin/docs`
- **ReDoc**: `http://your-server:8080/admin/redoc`

### Основные эндпоинты

#### Пользователи
- `GET /admin/users` - Список пользователей
- `GET /admin/users/{user_id}` - Детали пользователя
- `POST /admin/users/{user_id}/block` - Заблокировать пользователя
- `POST /admin/users/{user_id}/balance` - Изменить баланс

#### Подписки
- `GET /admin/subscriptions` - Список подписок
- `GET /admin/subscriptions/{id}` - Детали подписки
- `POST /admin/subscriptions/{id}/activate` - Активировать подписку

#### Настройки
- `GET /admin/settings` - Получить настройки
- `POST /admin/settings/update` - Обновить настройки

---

## 🛠️ Разработка

### Структура проекта

```
bot/handlers/       # Обработчики команд бота
bot/keyboards/      # Клавиатуры и inline-кнопки
bot/middleware/     # Middleware (логирование, rate limit)
bot/services/       # Бизнес-логика
admin/routes/       # API роуты админ-панели
admin/templates/    # HTML шаблоны
database/models.py  # Модели базы данных
api/marzban_api.py  # Клиент Marzban API
```

### Создание миграции

```bash
# Автоматическая генерация миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграции
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

### Тестирование

```bash
# Установка dev зависимостей
pip install -r requirements-dev.txt

# Запуск тестов
pytest

# С покрытием
pytest --cov=. --cov-report=html

# Линтеры
black .
isort .
flake8 .
mypy .
```

### Логирование

```python
from utils.logger import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## 🤝 Поддержка

### Документация
- 📖 [Wiki](https://github.com/yourusername/yovpn-bot/wiki)
- 📝 [FAQ](https://github.com/yourusername/yovpn-bot/wiki/FAQ)
- 🐛 [Issues](https://github.com/yourusername/yovpn-bot/issues)

### Контакты
- 💬 Telegram: [@YoVPNSupport](https://t.me/YoVPNSupport)
- 📧 Email: support@yovpn.com
- 🌐 Website: [yovpn.com](https://yovpn.com)

### Contributing

Мы приветствуем вклад в проект! Пожалуйста, прочитайте [CONTRIBUTING.md](CONTRIBUTING.md) перед отправкой PR.

---

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE).

---

## 🙏 Благодарности

- [aiogram](https://github.com/aiogram/aiogram) - Отличный фреймворк для Telegram ботов
- [FastAPI](https://github.com/tiangolo/fastapi) - Современный веб-фреймворк
- [Marzban](https://github.com/Gozargah/Marzban) - VPN панель управления
- [Tailwind CSS](https://tailwindcss.com/) - Утилитарный CSS фреймворк

---

<div align="center">

**Сделано с ❤️ для сообщества VPN**

⭐ Поставьте звезду если проект вам понравился!

</div>
