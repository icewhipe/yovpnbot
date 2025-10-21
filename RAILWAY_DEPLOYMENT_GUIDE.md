# 🚀 Полная Инструкция по Деплою на Railway

Полное руководство по развертыванию YoVPN (Бот + API + WebApp) на Railway.

## 📋 Содержание

1. [Подготовка](#1-подготовка)
2. [Вариант 1: Все на Railway (Рекомендуется)](#2-вариант-1-все-на-railway-рекомендуется)
3. [Вариант 2: WebApp на Vercel + Остальное на Railway](#3-вариант-2-webapp-на-vercel--остальное-на-railway)
4. [Настройка после деплоя](#4-настройка-после-деплоя)
5. [Проверка работоспособности](#5-проверка-работоспособности)
6. [Обновление приложения](#6-обновление-приложения)
7. [Troubleshooting](#7-troubleshooting)

---

## ⚠️ Важно: Исправление зависимостей

**Проблема с зависимостями уже исправлена!** ✅

Проект использует `requirements-prod.txt` для production деплоя, что исключает конфликты зависимостей.
Подробности в файле `RAILWAY_FIX_APPLIED.md`.

---

## 1. Подготовка

### 1.1 Создайте бота в Telegram

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям и получите токен бота
4. **Сохраните токен** - он понадобится для настройки

### 1.2 Получите данные от Marzban

Вам нужны:
- `MARZBAN_API_URL` - URL вашего Marzban сервера (например, `https://marzban.example.com`)
- `MARZBAN_USERNAME` - имя администратора
- `MARZBAN_PASSWORD` - пароль администратора

### 1.3 Сгенерируйте SECRET_KEY

```bash
# В терминале выполните:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Сохраните полученный ключ** - это ваш `SECRET_KEY`.

### 1.4 Зарегистрируйтесь на Railway

1. Откройте [railway.app](https://railway.app)
2. Зарегистрируйтесь через GitHub
3. Подтвердите email

---

## 2. Вариант 1: Все на Railway (Рекомендуется)

Этот вариант проще и дешевле - все компоненты на одной платформе.

### 2.1 Создание проекта на Railway

1. Откройте [railway.app/new](https://railway.app/new)
2. Нажмите **"Deploy from GitHub repo"**
3. Выберите ваш репозиторий с YoVPN
4. Нажмите **"Deploy Now"**

### 2.2 Добавление Redis (опционально, но рекомендуется)

1. В вашем проекте нажмите **"+ New"**
2. Выберите **"Database"** → **"Redis"**
3. Railway автоматически создаст Redis и переменную `REDIS_URL`

### 2.3 Настройка Telegram Bot Service

#### Шаг 1: Создайте сервис для бота

1. Нажмите **"+ New"** → **"Empty Service"**
2. Назовите сервис: `telegram-bot`

#### Шаг 2: Настройте Root Directory

1. Откройте настройки сервиса → **Settings**
2. В разделе **"Source"** установите:
   - **Root Directory**: оставьте пустым (корень проекта)
   - **Build Command**: оставьте пустым
   - **Start Command**: `python bot/main.py`

#### Шаг 3: Добавьте переменные окружения

В разделе **Variables** добавьте:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather

# Marzban
MARZBAN_API_URL=https://ваш-marzban-сервер.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=ваш_пароль

# Security
SECRET_KEY=ваш_сгенерированный_секретный_ключ

# Redis (если добавили)
REDIS_URL=${{Redis.REDIS_URL}}

# Database (SQLite по умолчанию)
SQLALCHEMY_DATABASE_URL=sqlite:///data/bot.db

# Python
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

#### Шаг 4: Настройте Dockerfile

Railway автоматически обнаружит `Dockerfile` в корне проекта.

### 2.4 Настройка API Service

#### Шаг 1: Создайте сервис для API

1. Нажмите **"+ New"** → **"Empty Service"**
2. Назовите сервис: `api`

#### Шаг 2: Настройте Root Directory

1. Settings → **Root Directory**: `api`
2. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Шаг 3: Добавьте переменные окружения

```env
# Telegram
TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather

# Security
SECRET_KEY=ваш_сгенерированный_секретный_ключ

# Marzban
MARZBAN_API_URL=https://ваш-marzban-сервер.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=ваш_пароль

# CORS (будет обновлено после деплоя webapp)
CORS_ORIGINS=*

# Redis (опционально)
REDIS_URL=${{Redis.REDIS_URL}}

# API Settings
API_HOST=0.0.0.0
API_PORT=$PORT
```

#### Шаг 4: Получите публичный URL API

1. Settings → **Networking**
2. Нажмите **"Generate Domain"**
3. **Сохраните URL** (например, `https://api-production-xxxx.up.railway.app`)

### 2.5 Настройка WebApp Service

#### Шаг 1: Создайте сервис для WebApp

1. Нажмите **"+ New"** → **"Empty Service"**
2. Назовите сервис: `webapp`

#### Шаг 2: Настройте Root Directory

1. Settings → **Root Directory**: `webapp`
2. **Build Command**: `npm install && npm run build`
3. **Start Command**: `npm start`

#### Шаг 3: Добавьте переменные окружения

```env
# Node
NODE_ENV=production

# Telegram
NEXT_PUBLIC_TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather

# API URL (используйте URL из шага 2.4)
NEXT_PUBLIC_API_BASE_URL=https://api-production-xxxx.up.railway.app

# WebApp URL (будет обновлено после генерации домена)
NEXT_PUBLIC_BASE_URL=https://webapp-production-yyyy.up.railway.app

# Dev Mode
NEXT_PUBLIC_DEV_MODE=false

# Download URLs (опционально, можете использовать свои)
NEXT_PUBLIC_ANDROID_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-android.apk
NEXT_PUBLIC_IOS_APP_STORE_URL=https://apps.apple.com/app/v2raytun
NEXT_PUBLIC_MACOS_DMG_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-macos.dmg
NEXT_PUBLIC_WINDOWS_EXE_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-windows.exe
NEXT_PUBLIC_ANDROID_TV_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-tv.apk
```

#### Шаг 4: Получите публичный URL WebApp

1. Settings → **Networking**
2. Нажмите **"Generate Domain"**
3. **Сохраните URL** (например, `https://webapp-production-yyyy.up.railway.app`)
4. **Обновите** переменную `NEXT_PUBLIC_BASE_URL` с этим URL

#### Шаг 5: Обновите CORS в API

Вернитесь к API сервису и обновите переменную `CORS_ORIGINS`:

```env
CORS_ORIGINS=https://webapp-production-yyyy.up.railway.app
```

### 2.6 Проверка всех сервисов

После деплоя у вас должно быть **4 активных сервиса**:

1. ✅ **Redis** - база данных для кэширования
2. ✅ **telegram-bot** - Telegram бот
3. ✅ **api** - Backend API
4. ✅ **webapp** - Frontend WebApp

---

## 3. Вариант 2: WebApp на Vercel + Остальное на Railway

Если вы хотите использовать Vercel для WebApp (бесплатный tier лучше подходит для Next.js).

### 3.1 Деплой на Railway (Бот + API)

Следуйте шагам **2.1 - 2.4** из Варианта 1 (Redis, Bot, API).

### 3.2 Деплой WebApp на Vercel

#### Шаг 1: Установите Vercel CLI

```bash
npm install -g vercel
```

#### Шаг 2: Войдите в Vercel

```bash
vercel login
```

#### Шаг 3: Настройте проект

1. Перейдите в папку webapp:
   ```bash
   cd webapp
   ```

2. Создайте файл `.env.production`:
   ```env
   NEXT_PUBLIC_TELEGRAM_BOT_TOKEN=ваш_токен
   NEXT_PUBLIC_API_BASE_URL=https://api-production-xxxx.up.railway.app
   NEXT_PUBLIC_BASE_URL=https://your-app.vercel.app
   NEXT_PUBLIC_DEV_MODE=false
   
   # Download URLs
   NEXT_PUBLIC_ANDROID_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-android.apk
   NEXT_PUBLIC_IOS_APP_STORE_URL=https://apps.apple.com/app/v2raytun
   NEXT_PUBLIC_MACOS_DMG_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-macos.dmg
   NEXT_PUBLIC_WINDOWS_EXE_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-windows.exe
   NEXT_PUBLIC_ANDROID_TV_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-tv.apk
   ```

#### Шаг 4: Деплой

```bash
vercel --prod
```

#### Шаг 5: Настройка через Dashboard

1. Откройте [vercel.com/dashboard](https://vercel.com/dashboard)
2. Выберите ваш проект
3. Settings → **Environment Variables**
4. Добавьте все переменные из `.env.production`

#### Шаг 6: Обновите CORS в Railway API

Вернитесь в Railway, откройте API сервис и обновите:

```env
CORS_ORIGINS=https://your-app.vercel.app
```

---

## 4. Настройка после деплоя

### 4.1 Обновите URL WebApp в боте

Если вы хотите, чтобы бот знал URL WebApp, можно добавить переменную окружения в **telegram-bot** сервис:

```env
WEBAPP_URL=https://webapp-production-yyyy.up.railway.app
# или
WEBAPP_URL=https://your-app.vercel.app
```

### 4.2 Настройка Menu Button в BotFather

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/mybots`
3. Выберите вашего бота
4. Нажмите **"Bot Settings"** → **"Menu Button"**
5. Введите URL WebApp:
   ```
   https://webapp-production-yyyy.up.railway.app
   ```
   или
   ```
   https://your-app.vercel.app
   ```

### 4.3 Настройка Custom Domain (опционально)

#### На Railway:

1. Купите домен (Namecheap, GoDaddy и т.д.)
2. В Railway: Settings → **Networking** → **Custom Domain**
3. Добавьте ваш домен (например, `bot.yourdomain.com`)
4. Настройте DNS записи:
   ```
   Type: CNAME
   Name: bot (или webapp, api)
   Value: указанный Railway CNAME
   ```

#### На Vercel:

1. Settings → **Domains** → **Add Domain**
2. Введите домен (например, `app.yourdomain.com`)
3. Настройте DNS согласно инструкциям Vercel

---

## 5. Проверка работоспособности

### 5.1 Проверка API

```bash
curl https://api-production-xxxx.up.railway.app/docs
```

Должна открыться документация Swagger.

### 5.2 Проверка WebApp

Откройте в браузере:
```
https://webapp-production-yyyy.up.railway.app
```

### 5.3 Проверка бота

1. Откройте вашего бота в Telegram
2. Отправьте команду `/start`
3. Бот должен ответить приветственным сообщением

### 5.4 Проверка логов

#### Railway:

1. Откройте любой сервис
2. Перейдите на вкладку **"Logs"**
3. Проверьте отсутствие ошибок

---

## 6. Обновление приложения

### 6.1 Автоматическое обновление (GitHub)

Railway автоматически обновляет приложение при push в репозиторий:

1. Внесите изменения в код
2. Сделайте commit и push:
   ```bash
   git add .
   git commit -m "Update bot"
   git push origin main
   ```
3. Railway автоматически пересоберет и задеплоит

### 6.2 Ручное обновление

В Railway Dashboard:

1. Откройте нужный сервис
2. Нажмите **"Deployments"**
3. Нажмите **"Redeploy"**

---

## 7. Troubleshooting

### 7.1 Бот не отвечает

**Проблема**: Бот не отвечает на команды

**Решение**:
1. Проверьте логи бота в Railway
2. Убедитесь, что `TELEGRAM_BOT_TOKEN` корректный
3. Проверьте, что сервис запущен (статус "Active")
4. Проверьте переменные окружения

### 7.2 API не отвечает

**Проблема**: WebApp не может подключиться к API

**Решение**:
1. Проверьте логи API сервиса
2. Убедитесь, что `NEXT_PUBLIC_API_BASE_URL` в WebApp указывает на правильный URL
3. Проверьте `CORS_ORIGINS` в API - должен содержать URL WebApp
4. Проверьте Health endpoint:
   ```bash
   curl https://api-production-xxxx.up.railway.app/health
   ```

### 7.3 WebApp не загружается

**Проблема**: WebApp показывает ошибку или не загружается

**Решение**:
1. Проверьте логи webapp сервиса
2. Убедитесь, что все `NEXT_PUBLIC_*` переменные установлены
3. Проверьте, что API доступен
4. Попробуйте пересобрать:
   ```bash
   # В Railway: Deployments → Redeploy
   ```

### 7.4 CORS ошибки

**Проблема**: Browser console показывает CORS ошибки

**Решение**:
1. Откройте API сервис в Railway
2. Проверьте переменную `CORS_ORIGINS`
3. Убедитесь, что она содержит точный URL WebApp (без trailing slash)
   ```env
   CORS_ORIGINS=https://webapp-production-yyyy.up.railway.app
   ```
4. Redeploy API сервиса

### 7.5 Проблемы с подключением к Marzban

**Проблема**: Бот не может подключиться к Marzban

**Решение**:
1. Проверьте `MARZBAN_API_URL` - должен быть полный URL с `https://`
2. Проверьте `MARZBAN_USERNAME` и `MARZBAN_PASSWORD`
3. Убедитесь, что Marzban сервер доступен из интернета
4. Проверьте логи бота для деталей ошибки

### 7.6 Build Failed

**Проблема**: Railway показывает "Build Failed"

**Решение**:
1. Проверьте логи деплоя
2. Убедитесь, что все зависимости в `requirements.txt` / `package.json`
3. Проверьте Root Directory в настройках
4. Для WebApp: убедитесь, что `npm install` успешно завершается

### 7.7 Out of Memory

**Проблема**: Сервис падает с ошибкой памяти

**Решение**:
1. На Railway бесплатный tier дает 512MB RAM
2. Рассмотрите upgrade до платного плана
3. Оптимизируйте код для меньшего использования памяти
4. Используйте Redis для кэширования

---

## 8. Мониторинг и обслуживание

### 8.1 Мониторинг в Railway

Railway предоставляет встроенный мониторинг:

1. Откройте любой сервис
2. Перейдите на вкладку **"Metrics"**
3. Отслеживайте:
   - CPU usage
   - Memory usage
   - Network traffic

### 8.2 Настройка Uptime мониторинга

Используйте бесплатные сервисы для мониторинга аптайма:

**UptimeRobot** ([uptimerobot.com](https://uptimerobot.com)):
1. Зарегистрируйтесь
2. Add New Monitor
3. Monitor Type: HTTP(s)
4. URL: `https://api-production-xxxx.up.railway.app/health`
5. Monitoring Interval: 5 minutes

**BetterUptime** ([betteruptime.com](https://betteruptime.com)):
1. Зарегистрируйтесь
2. Create Monitor
3. URL: ваш WebApp URL
4. Get notifications on Telegram/Email

### 8.3 Логирование

Все логи доступны в Railway Dashboard → Logs.

Для продакшена рекомендуется настроить внешнее логирование:

**Sentry** (для error tracking):
1. Зарегистрируйтесь на [sentry.io](https://sentry.io)
2. Создайте проект
3. Добавьте в переменные окружения:
   ```env
   SENTRY_DSN=ваш_sentry_dsn
   ```

---

## 9. Стоимость и лимиты

### Railway Pricing

**Hobby Plan** (Бесплатно):
- $5 бесплатно каждый месяц
- 512MB RAM на сервис
- 1GB Disk
- Shared CPU

**Developer Plan** ($5/месяц):
- $5 кредита включено
- 8GB RAM на сервис
- 100GB Disk
- Priority CPU

**Рекомендация**: Для production используйте Developer Plan.

### Vercel Pricing (если используете)

**Hobby Plan** (Бесплатно):
- 100GB bandwidth
- Unlimited deployments
- Serverless Functions

---

## 10. Чеклист перед запуском

- [ ] Все переменные окружения установлены
- [ ] Все сервисы показывают статус "Active"
- [ ] API доступен и отвечает на `/health`
- [ ] WebApp загружается
- [ ] Бот отвечает на `/start`
- [ ] CORS настроен правильно
- [ ] Menu Button настроен в BotFather
- [ ] Домены настроены (если используете)
- [ ] Uptime мониторинг настроен
- [ ] Логи проверены на ошибки

---

## 11. Полезные ссылки

- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Aiogram Documentation](https://docs.aiogram.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 12. Поддержка

Если у вас возникли проблемы:

1. Проверьте логи в Railway/Vercel
2. Убедитесь, что все переменные окружения корректны
3. Проверьте этот troubleshooting раздел
4. Создайте issue на GitHub

---

**Успешного деплоя! 🚀**

---

## Краткая инструкция (TL;DR)

### Railway (все в одном месте)

1. **Подготовка**:
   - Получите токен бота от BotFather
   - Сгенерируйте SECRET_KEY
   - Подготовьте данные Marzban

2. **Railway Setup**:
   - Создайте проект из GitHub репозитория
   - Добавьте 4 сервиса: Redis, telegram-bot, api, webapp
   - Настройте переменные окружения для каждого
   - Сгенерируйте публичные URL для api и webapp

3. **Post-Deploy**:
   - Обновите CORS_ORIGINS в API с URL WebApp
   - Настройте Menu Button в BotFather
   - Проверьте работу бота командой /start

4. **Готово!** ✨

Весь процесс занимает ~20-30 минут.
