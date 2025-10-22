# 🚀 YoVPN — Современный Telegram VPN-бот с WebApp

<div align="center">

![YoVPN Banner](https://img.shields.io/badge/YoVPN-v2.0-blue?style=for-the-badge&logo=telegram)

**Полнофункциональный VPN-бот для Telegram с WebApp интерфейсом**

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat&logo=next.js)](https://nextjs.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3-blue?style=flat&logo=telegram)](https://docs.aiogram.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![Railway](https://img.shields.io/badge/Railway-Deploy-0B0D0E?style=flat&logo=railway)](https://railway.app)

[🚀 Быстрый старт](#-быстрый-старт) • [📖 Документация](#-документация) • [🌐 Деплой](#-деплой-на-railway) • [💬 Поддержка](#-поддержка)

</div>

---

## 📋 Оглавление

- [О проекте](#-о-проекте)
- [Особенности](#-особенности)
- [Технологии](#-технологии)
- [Быстрый старт](#-быстрый-старт)
- [Структура проекта](#-структура-проекта)
- [Деплой на Railway](#-деплой-на-railway)
- [Настройка](#-настройка)
- [Документация](#-документация)
- [Типичные ошибки](#-типичные-ошибки)
- [Поддержка](#-поддержка)
- [Лицензия](#-лицензия)

---

## 🎯 О проекте

**YoVPN** — это современное решение для продажи VPN-подписок через Telegram, включающее:

- 🤖 **Telegram Bot** — интуитивный интерфейс с красивым меню
- 🌐 **WebApp** — Telegram Mini App для активации подписок
- ⚡ **API** — FastAPI backend для управления данными
- 💳 **Платежи** — интеграция с ЮKassa, Stripe, криптовалютой
- 🔐 **Marzban** — интеграция с VPN-панелью управления
- 📊 **Аналитика** — статистика пользователей и продаж

### 🎬 Как это работает?

```
Пользователь → Telegram Bot → Оплата → Активация → VPN подписка
                    ↓
              Telegram WebApp
                    ↓
            Выбор платформы → Скачивание → Автоактивация
```

---

## ✨ Особенности

### 🎨 Современный UX/UI (тренды 2025-2026)

| Компонент | Описание |
|-----------|----------|
| **Минималистичное меню** | Чистые кнопки, понятные иконки, без перегрузки |
| **Красивые тексты** | Quote-блоки, code-форматирование, эмодзи |
| **Анимация загрузки** | Прогресс-бары при инициализации |
| **Компактность** | InlineKeyboard вместо ReplyKeyboard |
| **Умная навигация** | Хлебные крошки, кнопка "Назад" |

### 🚀 Технические возможности

- ✅ **Многоязычность** (готово к i18n)
- ✅ **Реферальная программа** (автоматические бонусы)
- ✅ **Автопродление** подписок
- ✅ **Admin-панель** через бота
- ✅ **Webhook / Long Polling**
- ✅ **Docker + Docker Compose**
- ✅ **Railway-ready** (1-click deploy)
- ✅ **Тесты** (pytest для бэкенда)

### 📱 WebApp функции

- **1-Click Activation** — подписка активируется в 1 клик
- **Кросс-платформенность** — Android, iOS, macOS, Windows, Android TV
- **PWA** — работает как нативное приложение
- **GSAP анимации** — плавные переходы
- **Dev Mode** — тестирование без Telegram

---

## 🛠️ Технологии

### Backend

- **Python 3.11+** — основной язык
- **aiogram 3** — Telegram Bot Framework
- **FastAPI** — API фреймворк
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **Pydantic** — валидация данных

### Frontend (WebApp)

- **Next.js 15** — React фреймворк
- **TypeScript 5** — типизация
- **Tailwind CSS 3** — стили
- **GSAP 3** — анимации
- **Zustand** — state management
- **Axios** — HTTP клиент

### DevOps

- **Docker** — контейнеризация
- **Docker Compose** — оркестрация
- **Railway** — хостинг
- **Nginx** — reverse proxy
- **GitHub Actions** — CI/CD

---

## 🚀 Быстрый старт

### Требования

- **Node.js 18+**
- **Python 3.11+**
- **PostgreSQL 15+**
- **Git**

### Автоматическая установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/yourusername/yovpn.git
cd yovpn

# 2. Запустите установку
chmod +x install.sh
./install.sh

# 3. Настройте .env
cp .env.example .env
nano .env  # Добавьте TELEGRAM_BOT_TOKEN и другие переменные

# 4. Запустите всё
./start-webapp.sh
```

**Готово!** 🎉

- 🤖 Бот работает
- 🌐 WebApp: http://localhost:3000
- ⚡ API: http://localhost:8000/docs

### Ручная установка

См. подробную инструкцию: **[QUICK_START.md](./QUICK_START.md)**

---

## 📁 Структура проекта

```
yovpn/
├── 🤖 bot/                         # Telegram Bot
│   ├── handlers/                   # Обработчики команд
│   │   ├── start_handler.py        # /start
│   │   ├── menu_handler.py         # Главное меню
│   │   ├── payment_handler.py      # Платежи
│   │   └── subscription_handler.py # Подписки
│   ├── keyboards/                  # Клавиатуры
│   │   └── menu_kb.py              # Меню (InlineKeyboard)
│   ├── services/                   # Сервисы
│   │   ├── user_service.py         # Работа с пользователями
│   │   ├── payment_service.py      # Платежи
│   │   └── animation_service.py    # Анимации
│   ├── middleware/                 # Middleware
│   └── main.py                     # Точка входа
│
├── 🌐 webapp/                      # Next.js WebApp
│   ├── src/
│   │   ├── app/                    # App Router
│   │   ├── components/             # React компоненты
│   │   ├── hooks/                  # useTelegram, useStore
│   │   └── lib/                    # API, utils, constants
│   └── Dockerfile
│
├── ⚡ api/                          # FastAPI Backend
│   ├── app/
│   │   ├── routes/                 # API endpoints
│   │   ├── services/               # Бизнес-логика
│   │   └── models/                 # Pydantic модели
│   └── Dockerfile
│
├── 🐳 docker-compose.yml           # Docker Compose
├── 📋 requirements.txt             # Python зависимости
├── 🔐 .env.example                 # Пример переменных
└── 📖 README.md                    # Этот файл
```

---

## 🌐 Деплой на Railway

### Быстрый деплой (5 минут)

Railway — самый простой способ задеплоить YoVPN.

#### Шаг 1: Подготовка

```bash
# Создайте репозиторий на GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/yovpn.git
git push -u origin main
```

#### Шаг 2: Railway Dashboard

1. Откройте [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub repo**
3. Выберите `yovpn`

#### Шаг 3: Создайте 3 сервиса

**Сервис 1: WebApp**
- Root Directory: `/webapp`
- Builder: DOCKERFILE
- Переменные: `NEXT_PUBLIC_API_URL`, `PORT=3000`

**Сервис 2: API**
- Root Directory: `/api`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Переменные: `DATABASE_URL`, `TELEGRAM_BOT_TOKEN`

**Сервис 3: Bot**
- Root Directory: `/`
- Start Command: `python -m bot.main`
- Переменные: `TELEGRAM_BOT_TOKEN`, `API_URL`, `WEBAPP_URL`

#### Шаг 4: Добавьте PostgreSQL

Railway → **New Service** → **PostgreSQL**

Переменная `DATABASE_URL` создастся автоматически.

#### Шаг 5: Deploy!

```bash
git push origin main
```

Railway автоматически задеплоит все сервисы.

### Полное руководство

**Исчерпывающая инструкция с исправлением всех ошибок:**

📖 **[RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md](./RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md)**

---

## ⚙️ Настройка

### Переменные окружения

Создайте `.env` в корне проекта:

```env
# ═══════════════════════════════════════════
# 🤖 TELEGRAM BOT
# ═══════════════════════════════════════════
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHI...
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890...

# ═══════════════════════════════════════════
# 🐘 DATABASE
# ═══════════════════════════════════════════
DATABASE_URL=postgresql://user:password@localhost:5432/yovpn

# ═══════════════════════════════════════════
# 🔐 MARZBAN (VPN Panel)
# ═══════════════════════════════════════════
MARZBAN_URL=https://your-marzban.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=your-password

# ═══════════════════════════════════════════
# 🌐 SERVICES
# ═══════════════════════════════════════════
API_URL=http://localhost:8000
WEBAPP_URL=http://localhost:3000

# ═══════════════════════════════════════════
# ⚙️ SETTINGS
# ═══════════════════════════════════════════
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Получение токенов

#### TELEGRAM_BOT_TOKEN

1. [@BotFather](https://t.me/BotFather)
2. `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

#### TELEGRAM_API_ID и API_HASH

1. [my.telegram.org/apps](https://my.telegram.org/apps)
2. Войдите
3. Создайте приложение
4. Скопируйте API ID и Hash

---

## 📖 Документация

### Основные документы

| Документ | Описание |
|----------|----------|
| **[QUICK_START.md](./QUICK_START.md)** | Быстрый старт (подробно) |
| **[RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md](./RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md)** | Полный гайд по деплою |
| **[WEBAPP_GUIDE.md](./WEBAPP_GUIDE.md)** | Документация WebApp |
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Архитектура проекта |
| **[CONTRIBUTING.md](./CONTRIBUTING.md)** | Как контрибутить |
| **[CHANGELOG.md](./CHANGELOG.md)** | История изменений |

### API Документация

После запуска откройте:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Примеры использования

**Python (bot):**

```python
from bot.services.user_service import UserService

# Создать пользователя
user = await user_service.create_or_update_user(
    user_id=123456789,
    username="john_doe",
    first_name="John"
)

# Получить баланс
balance = await user_service.get_balance(user_id=123456789)
```

**TypeScript (webapp):**

```typescript
import { useTelegram } from '@/hooks/useTelegram';

const { webApp, user } = useTelegram();

// Получить данные пользователя
console.log(user?.id);        // 123456789
console.log(user?.first_name); // John

// Haptic feedback
webApp?.HapticFeedback.impactOccurred('medium');
```

---

## ❌ Типичные ошибки

### 1. `sh: next: not found`

**Причина:** Неправильная команда запуска в Dockerfile

**Решение:**

```dockerfile
# ✅ ПРАВИЛЬНО
CMD ["node", "server.js"]

# ❌ НЕПРАВИЛЬНО
CMD ["npm", "start"]  # или
CMD ["next", "start"]
```

Также убедитесь:
- `next` в `dependencies` (не в `devDependencies`)
- `output: 'standalone'` в `next.config.js`

**Подробнее:** [RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md](./RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md#-исправление-ошибки-sh-next-not-found)

### 2. Бот не отвечает

**Проверьте:**

1. Токен правильный?
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getMe
   ```

2. Бот запущен?
   ```bash
   ps aux | grep "python -m bot.main"
   ```

3. Логи без ошибок?
   ```bash
   tail -f logs/bot.log
   ```

### 3. WebApp не открывается

**Telegram требует HTTPS!**

Для локального тестирования используйте ngrok:

```bash
ngrok http 3000
# Обновите WEBAPP_URL на https://xxxxx.ngrok.io
```

### 4. DATABASE_URL ошибка

**Правильный формат:**

```
postgresql://user:password@host:port/database
```

**Railway:** Используйте `${{Postgres.DATABASE_URL}}`

### 5. CORS ошибки

API должен разрешать запросы от WebApp:

```python
# api/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-webapp.railway.app",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 Тестирование

### Запуск тестов

```bash
# Backend тесты
pytest

# Frontend тесты
cd webapp && npm test

# E2E тесты
npm run test:e2e
```

### Coverage

```bash
# Backend
pytest --cov=bot --cov=api --cov-report=html

# Frontend
npm run test:coverage
```

---

## 🤝 Contributing

Contributions приветствуются! 🎉

1. Fork проекта
2. Создайте feature branch: `git checkout -b feature/amazing`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing`
5. Откройте Pull Request

См. [CONTRIBUTING.md](./CONTRIBUTING.md) для деталей.

---

## 💬 Поддержка

### Нужна помощь?

- 📖 **Документация:** [QUICK_START.md](./QUICK_START.md)
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/yourusername/yovpn/issues)
- 💬 **Telegram:** [@yovpn_support](https://t.me/yovpn_support)
- ✉️ **Email:** support@yovpn.com

### FAQ

**Q: Как добавить нового админа?**

```python
# bot/handlers/admin_handler.py
ADMIN_IDS = [123456789, 987654321]
```

**Q: Как изменить тексты бота?**

Все тексты в `bot/utils/texts.py`

**Q: Как добавить новую платформу в WebApp?**

См. [WEBAPP_GUIDE.md](./WEBAPP_GUIDE.md#добавление-новой-платформы)

---

## 📄 Лицензия

MIT License — см. [LICENSE](./LICENSE)

```
Copyright (c) 2025 YoVPN Team

Permission is hereby granted, free of charge...
```

---

## 🙏 Благодарности

Проект использует:

- [aiogram](https://docs.aiogram.dev/) — Telegram Bot Framework
- [Next.js](https://nextjs.org/) — React Framework
- [FastAPI](https://fastapi.tiangolo.com/) — Python Web Framework
- [Railway](https://railway.app/) — Hosting Platform

Особая благодарность:
- Telegram Team за Bot API
- Next.js Team за потрясающий фреймворк
- Railway Team за простой деплой

---

## 🗺️ Roadmap

### ✅ v1.0 (Текущая)

- [x] Telegram Bot с современным меню
- [x] WebApp (Telegram Mini App)
- [x] FastAPI Backend
- [x] PostgreSQL интеграция
- [x] Marzban интеграция
- [x] Реферальная программа
- [x] Docker + Docker Compose
- [x] Railway деплой

### 🚧 v1.1 (В разработке)

- [ ] Мультиязычность (i18n)
- [ ] Push-уведомления
- [ ] Admin Dashboard (WebApp)
- [ ] Расширенная аналитика
- [ ] A/B тестирование

### 🔮 v2.0 (Планируется)

- [ ] Crypto payments
- [ ] Subscription plans
- [ ] Affiliate program
- [ ] Mobile apps (React Native)
- [ ] White-label solution

---

<div align="center">

## ⭐ Star нас на GitHub!

Если проект оказался полезным, поставьте звезду ⭐

[![GitHub stars](https://img.shields.io/github/stars/yourusername/yovpn?style=social)](https://github.com/yourusername/yovpn/stargazers)

---

**Создано с ❤️ YoVPN Team**

*Современный VPN-сервис с фокусом на UX & безопасность*

[📖 Документация](./QUICK_START.md) • [🚀 Деплой](./RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md) • [💬 Поддержка](#-поддержка)

</div>
