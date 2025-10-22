# 🚀 Полное руководство по деплою на Railway

> **Версия:** 2.0 (Обновлено: 22.10.2025)  
> **Статус:** ✅ Протестировано и работает

---

## 📋 Оглавление

1. [Предварительные требования](#-предварительные-требования)
2. [Исправление ошибки `sh: next: not found`](#-исправление-ошибки-sh-next-not-found)
3. [Деплой WebApp (Next.js)](#-деплой-webapp-nextjs)
4. [Деплой API (FastAPI)](#-деплой-api-fastapi)
5. [Деплой Бота (aiogram)](#-деплой-бота-aiogram)
6. [Настройка переменных окружения](#-настройка-переменных-окружения)
7. [Типичные ошибки и их решение](#-типичные-ошибки-и-их-решение)
8. [Мониторинг и логи](#-мониторинг-и-логи)

---

## ✅ Предварительные требования

### 1. Аккаунт на Railway

1. Перейдите на [railway.app](https://railway.app)
2. Зарегистрируйтесь через GitHub
3. Подтвердите email

### 2. GitHub репозиторий

Убедитесь, что ваш проект загружен на GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/yovpn.git
git push -u origin main
```

### 3. Переменные окружения

Подготовьте следующие переменные:

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890

# Database (Railway предоставляет автоматически)
DATABASE_URL=postgresql://user:password@host:port/database

# API
API_URL=https://your-api.railway.app
WEBAPP_URL=https://your-webapp.railway.app

# Marzban (если используете)
MARZBAN_URL=https://your-marzban.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=your-password
```

---

## 🔧 Исправление ошибки `sh: next: not found`

### Причина ошибки

Ошибка возникает, когда:
1. `next` не установлен в `dependencies` (находится в `devDependencies`)
2. Неправильная команда запуска в Dockerfile
3. `node_modules` не копируются в production образ

### ✅ Решение (уже применено)

Обновленный `webapp/Dockerfile`:

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Disable telemetry
ENV NEXT_TELEMETRY_DISABLED 1

# Build the application
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# ✅ ПРАВИЛЬНАЯ КОМАНДА (не `next start`)
CMD ["node", "server.js"]
```

### Проверка `package.json`

Убедитесь, что `next` в `dependencies`:

```json
{
  "dependencies": {
    "next": "^15.0.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }
}
```

### Проверка `next.config.js`

Убедитесь, что включен standalone режим:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone', // ✅ ОБЯЗАТЕЛЬНО для Docker
  reactStrictMode: true,
}

module.exports = nextConfig
```

---

## 🌐 Деплой WebApp (Next.js)

### Шаг 1: Создать новый проект на Railway

1. Откройте [railway.app/new](https://railway.app/new)
2. **Deploy from GitHub repo**
3. Выберите ваш репозиторий `yovpn`
4. Назовите сервис: `yovpn-webapp`

### Шаг 2: Настройка деплоя

В настройках проекта:

1. **Root Directory**: `/webapp`
2. **Build Command**: `npm run build`
3. **Start Command**: оставьте пустым (используется Dockerfile)

### Шаг 3: Настройка Dockerfile

Railway автоматически обнаружит `webapp/Dockerfile`.

Если нет, добавьте в корень `/webapp/railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
```

### Шаг 4: Добавить переменные окружения

В Railway Dashboard → Variables:

```env
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://your-api.railway.app
NEXT_PUBLIC_BOT_USERNAME=your_bot
PORT=3000
```

### Шаг 5: Deploy!

```bash
# Railway автоматически деплоит при каждом push
git add .
git commit -m "Deploy webapp to Railway"
git push origin main
```

### Шаг 6: Проверка

1. Railway покажет URL: `https://yovpn-webapp-production.up.railway.app`
2. Откройте URL в браузере
3. Проверьте логи:

```
Railway Dashboard → yovpn-webapp → Logs
```

**Ожидаемый вывод:**

```
✓ Ready in 2.1s
✓ Compiled successfully
Server ready on http://0.0.0.0:3000
```

**❌ НЕ ДОЛЖНО БЫТЬ:**

```
sh: next: not found  ❌
```

---

## 🔌 Деплой API (FastAPI)

### Шаг 1: Создать новый сервис

1. Railway Dashboard → **New Service**
2. **Deploy from GitHub repo** → выберите тот же репозиторий
3. Назовите: `yovpn-api`

### Шаг 2: Настройка

1. **Root Directory**: `/api`
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Шаг 3: Переменные окружения

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHI...
MARZBAN_URL=https://your-marzban.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=your-password
WEBAPP_URL=https://yovpn-webapp-production.up.railway.app
PORT=8000
```

### Шаг 4: Добавить PostgreSQL (опционально)

1. Railway Dashboard → **New Service**
2. **Add PostgreSQL**
3. Railway автоматически создаст `DATABASE_URL`
4. Используйте переменную: `${{Postgres.DATABASE_URL}}`

### Шаг 5: Deploy

```bash
git push origin main
```

### Шаг 6: Проверка

Откройте: `https://your-api.railway.app/docs`

Должен открыться Swagger UI с документацией API.

---

## 🤖 Деплой Бота (aiogram)

### Шаг 1: Создать новый сервис

1. Railway Dashboard → **New Service**
2. **Deploy from GitHub repo**
3. Назовите: `yovpn-bot`

### Шаг 2: Настройка

1. **Root Directory**: `/` (корень проекта)
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python -m bot.main`

Или создайте `railway.json` в корне:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "startCommand": "python -m bot.main"
  }
}
```

### Шаг 3: Переменные окружения

```env
TELEGRAM_BOT_TOKEN=1234567890:ABC...
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef...
DATABASE_URL=${{Postgres.DATABASE_URL}}
API_URL=https://your-api.railway.app
WEBAPP_URL=https://your-webapp.railway.app
MARZBAN_URL=https://your-marzban.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=your-password
```

### Шаг 4: Deploy

```bash
git push origin main
```

### Шаг 5: Проверка логов

Railway → yovpn-bot → Logs

**Ожидаемый вывод:**

```
INFO:bot.main:🚀 Запуск бота...
INFO:bot.main:✅ Бот успешно запущен
INFO:aiogram:Bot @your_bot_name started
```

---

## 🔐 Настройка переменных окружения

### Для WebApp

```env
# Next.js Public Variables (доступны в браузере)
NEXT_PUBLIC_API_URL=https://your-api.railway.app
NEXT_PUBLIC_BOT_USERNAME=your_bot
NEXT_PUBLIC_WEBAPP_URL=https://your-webapp.railway.app

# Server-side Variables
NODE_ENV=production
PORT=3000
```

### Для API

```env
# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABC...

# Marzban
MARZBAN_URL=https://your-marzban.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=your-password

# URLs
WEBAPP_URL=https://your-webapp.railway.app

# Server
PORT=8000
ENVIRONMENT=production
```

### Для Бота

```env
# Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABC...
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef...

# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Services
API_URL=https://your-api.railway.app
WEBAPP_URL=https://your-webapp.railway.app
MARZBAN_URL=https://your-marzban.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=your-password

# Settings
ENVIRONMENT=production
LOG_LEVEL=INFO
```

---

## ❌ Типичные ошибки и их решение

### 1. `sh: next: not found`

**Причина:** Неправильная команда запуска или `next` в `devDependencies`

**Решение:**
1. Проверьте `package.json` - `next` должен быть в `dependencies`
2. В Dockerfile используйте `CMD ["node", "server.js"]` вместо `next start`
3. Убедитесь, что `output: 'standalone'` в `next.config.js`

### 2. `Module not found: Can't resolve 'next'`

**Причина:** `node_modules` не копируются в production образ

**Решение:**
```dockerfile
# В builder stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build
```

### 3. `Error: ENOENT: no such file or directory, open 'server.js'`

**Причина:** Standalone режим не создал `server.js`

**Решение:**
Проверьте `next.config.js`:
```javascript
output: 'standalone',
```

Пересоберите:
```bash
npm run build
ls .next/standalone  # должен быть server.js
```

### 4. `Failed to load SWC binary`

**Причина:** Несовместимая архитектура (Apple Silicon / x86)

**Решение:**
В `package.json` добавьте:
```json
{
  "optionalDependencies": {
    "@next/swc-linux-x64-gnu": "^15.0.2",
    "@next/swc-linux-x64-musl": "^15.0.2"
  }
}
```

### 5. Railway build timeout

**Причина:** Долгая сборка (особенно для Next.js)

**Решение:**
1. Используйте `.dockerignore`:
```
node_modules
.next
.git
*.md
```

2. Оптимизируйте `npm ci` вместо `npm install`

### 6. `Cannot find module 'bot/main'`

**Причина:** Неправильный Root Directory

**Решение:**
- Для бота Root Directory = `/` (корень)
- Для API Root Directory = `/api`
- Для WebApp Root Directory = `/webapp`

### 7. PostgreSQL connection failed

**Причина:** Неправильный формат `DATABASE_URL`

**Решение:**
Используйте Railway reference:
```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Не хардкодьте URL!

### 8. CORS errors в WebApp

**Причина:** API не разрешает запросы с Railway домена

**Решение:**
В `api/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-webapp.railway.app",
        "https://*.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Мониторинг и логи

### Просмотр логов

Railway Dashboard → Сервис → **Logs**

### Полезные команды для логов

**Бот:**
```python
import logging
logger = logging.getLogger(__name__)
logger.info("✅ Все работает")
logger.error("❌ Ошибка!")
```

**API:**
```python
import logging
logging.info("API endpoint called")
```

**WebApp (в Railway):**
```bash
console.log("WebApp loaded")
# Логи будут в Railway Dashboard
```

### Health Checks

Railway автоматически проверяет здоровье сервиса.

**Для API** добавьте эндпоинт:
```python
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**Для WebApp** Railway пингует `/`

### Метрики

Railway → Service → **Metrics**

Показывает:
- CPU usage
- Memory usage
- Network traffic
- Response time

---

## 🎯 Чек-лист перед деплоем

### WebApp
- [ ] `next` в `dependencies`, не в `devDependencies`
- [ ] `output: 'standalone'` в `next.config.js`
- [ ] Dockerfile использует `CMD ["node", "server.js"]`
- [ ] Все переменные `NEXT_PUBLIC_*` настроены
- [ ] `.dockerignore` создан
- [ ] `npm run build` работает локально

### API
- [ ] `requirements.txt` актуален
- [ ] `DATABASE_URL` настроен
- [ ] CORS middleware настроен
- [ ] Health check эндпоинт `/health` добавлен
- [ ] Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Бот
- [ ] `TELEGRAM_BOT_TOKEN` настроен
- [ ] Root directory = `/` (корень проекта)
- [ ] Start command: `python -m bot.main`
- [ ] `DATABASE_URL` настроен
- [ ] Все сервисы (API, WebApp) доступны

---

## 🚀 Итоговая проверка

После деплоя всех 3 сервисов:

### 1. WebApp
```bash
curl https://your-webapp.railway.app
# Должен вернуть HTML страницу
```

### 2. API
```bash
curl https://your-api.railway.app/health
# {"status":"healthy"}
```

### 3. Бот
Отправьте `/start` боту в Telegram.

Должен ответить приветственным сообщением.

---

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте логи в Railway Dashboard
2. Посмотрите [Railway Docs](https://docs.railway.app/)
3. Откройте Issue на GitHub
4. Telegram: @yovpn_support

---

## ✅ Успех!

Если все 3 сервиса работают:

- ✅ WebApp открывается
- ✅ API возвращает данные
- ✅ Бот отвечает на команды

**Поздравляем! Ваш проект успешно задеплоен на Railway! 🎉**

---

**Дата обновления:** 22.10.2025  
**Автор:** YoVPN Team  
**Лицензия:** MIT
