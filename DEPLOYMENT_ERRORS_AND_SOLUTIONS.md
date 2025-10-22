# ⚠️ Типичные ошибки при деплое и их решения

> **Обновлено:** 22.10.2025  
> **Версия:** 2.0

Этот документ содержит **все возможные ошибки**, с которыми вы можете столкнуться при деплое YoVPN на Railway или другие платформы, и их **готовые решения**.

---

## 📋 Оглавление

1. [Ошибки WebApp (Next.js)](#-ошибки-webapp-nextjs)
2. [Ошибки API (FastAPI)](#-ошибки-api-fastapi)
3. [Ошибки бота (aiogram)](#-ошибки-бота-aiogram)
4. [Ошибки базы данных](#-ошибки-базы-данных)
5. [Ошибки Docker](#-ошибки-docker)
6. [Ошибки Railway](#-ошибки-railway)
7. [Сетевые ошибки](#-сетевые-ошибки)

---

## 🌐 Ошибки WebApp (Next.js)

### 1. `sh: next: not found`

**Ошибка:**
```
sh: 1: next: not found
```

**Причина:**
- `next` находится в `devDependencies` вместо `dependencies`
- Неправильная команда запуска в Dockerfile
- `node_modules` не копируются в production образ

**Решение:**

#### Шаг 1: Проверьте `package.json`

```json
{
  "dependencies": {
    "next": "^15.0.2",    // ✅ ДОЛЖЕН БЫТЬ ЗДЕСЬ
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    // ❌ next НЕ ДОЛЖЕН БЫТЬ ЗДЕСЬ
  }
}
```

#### Шаг 2: Проверьте `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',  // ✅ ОБЯЗАТЕЛЬНО для Docker
  reactStrictMode: true,
}

module.exports = nextConfig
```

#### Шаг 3: Проверьте `Dockerfile`

```dockerfile
# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

# ✅ ПРАВИЛЬНАЯ КОМАНДА (не next start!)
CMD ["node", "server.js"]

# ❌ НЕПРАВИЛЬНО:
# CMD ["npm", "start"]
# CMD ["next", "start"]
```

#### Шаг 4: Пересоберите

```bash
cd webapp
npm install
npm run build

# Проверьте, что server.js создан
ls .next/standalone/server.js  # Должен существовать
```

---

### 2. `Module not found: Can't resolve 'next'`

**Ошибка:**
```
Module not found: Can't resolve 'next'
```

**Причина:**
`node_modules` не копируются в builder stage

**Решение:**

```dockerfile
# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app

# ✅ Копируем node_modules из deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build
```

---

### 3. `Error: ENOENT: no such file or directory, open 'server.js'`

**Ошибка:**
```
Error: ENOENT: no such file or directory, open '/app/server.js'
```

**Причина:**
Standalone режим не создал `server.js`

**Решение:**

1. Проверьте `next.config.js`:
```javascript
output: 'standalone',  // Должно быть включено
```

2. Пересоберите:
```bash
rm -rf .next
npm run build
ls .next/standalone  # Проверьте server.js
```

3. Если `server.js` всё ещё нет:
```bash
# Обновите Next.js
npm install next@latest

# Очистите кэш
rm -rf node_modules .next
npm install
npm run build
```

---

### 4. `Failed to load SWC binary`

**Ошибка:**
```
Error: Failed to load SWC binary for linux/x64
```

**Причина:**
Несовместимая архитектура (Apple Silicon / x86)

**Решение:**

Добавьте в `package.json`:

```json
{
  "optionalDependencies": {
    "@next/swc-linux-x64-gnu": "^15.0.2",
    "@next/swc-linux-x64-musl": "^15.0.2",
    "@next/swc-darwin-arm64": "^15.0.2",
    "@next/swc-darwin-x64": "^15.0.2"
  }
}
```

---

### 5. Railway build timeout

**Ошибка:**
```
Build timed out after 10 minutes
```

**Причина:**
Долгая сборка из-за больших файлов

**Решение:**

Создайте `.dockerignore`:

```
node_modules
.next
.git
.env*
*.md
*.log
.DS_Store
dist
build
coverage
```

Оптимизируйте установку:

```dockerfile
# Используйте ci вместо install
RUN npm ci --only=production
```

---

## ⚡ Ошибки API (FastAPI)

### 1. `ModuleNotFoundError: No module named 'fastapi'`

**Ошибка:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Причина:**
Зависимости не установлены

**Решение:**

```bash
pip install -r requirements.txt

# Для Railway добавьте в настройках:
# Build Command: pip install -r requirements.txt
```

---

### 2. `Error: Unable to find application`

**Ошибка:**
```
Error: Unable to find application in 'app.main:app'
```

**Причина:**
Неправильный путь к приложению

**Решение:**

Проверьте структуру:
```
api/
├── app/
│   └── main.py  # app = FastAPI()
```

Start Command должен быть:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Для Railway:
- Root Directory: `/api`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

### 3. CORS errors

**Ошибка:**
```
Access to fetch at 'https://api.railway.app' from origin 'https://webapp.railway.app' has been blocked by CORS
```

**Причина:**
CORS не настроен

**Решение:**

```python
# api/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-webapp.railway.app",
        "https://*.up.railway.app",  # Все Railway поддомены
        "http://localhost:3000",     # Локальная разработка
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 4. `sqlalchemy.exc.OperationalError: connection refused`

**Ошибка:**
```
sqlalchemy.exc.OperationalError: could not connect to server: Connection refused
```

**Причина:**
Неправильный `DATABASE_URL`

**Решение:**

1. **Локально:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/yovpn
```

2. **Railway:**
```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

3. **Проверьте формат:**
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

4. **Тест подключения:**
```python
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
connection = engine.connect()
print("✅ Connected!")
```

---

## 🤖 Ошибки бота (aiogram)

### 1. `Unauthorized: Invalid token`

**Ошибка:**
```
aiogram.exceptions.TelegramUnauthorizedError: Telegram server says - Unauthorized: Invalid token
```

**Причина:**
Неправильный `TELEGRAM_BOT_TOKEN`

**Решение:**

1. Проверьте токен в [@BotFather](https://t.me/BotFather):
```
/token
```

2. Формат токена:
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567890
```

3. Проверьте `.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...  # Без пробелов!
```

4. Тест токена:
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

Должен вернуть:
```json
{
  "ok": true,
  "result": {
    "id": 123456789,
    "is_bot": true,
    "first_name": "YoVPN Bot",
    "username": "yovpn_bot"
  }
}
```

---

### 2. `Cannot find module 'bot.main'`

**Ошибка:**
```
ModuleNotFoundError: No module named 'bot.main'
```

**Причина:**
Неправильный Root Directory в Railway

**Решение:**

Railway настройки:
- **Root Directory:** `/` (корень проекта, НЕ `/bot`)
- **Start Command:** `python -m bot.main`

Проверьте структуру:
```
/
├── bot/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
```

---

### 3. Бот не отвечает на команды

**Причина:**
- Бот не запущен
- Webhook конфликт
- Неправильные handlers

**Решение:**

1. **Проверьте, что бот запущен:**
```bash
ps aux | grep "python -m bot.main"
```

2. **Удалите webhook (если есть):**
```bash
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook
```

3. **Проверьте логи:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

4. **Проверьте регистрацию handlers:**
```python
# bot/main.py
from bot.handlers import start_handler

dp.include_router(start_handler.router)
```

---

## 🐘 Ошибки базы данных

### 1. `relation "users" does not exist`

**Ошибка:**
```
sqlalchemy.exc.ProgrammingError: relation "users" does not exist
```

**Причина:**
Миграции не применены

**Решение:**

```bash
# Alembic
alembic upgrade head

# Или создайте таблицы программно
python -c "from app.models import Base; from app.database import engine; Base.metadata.create_all(engine)"
```

---

### 2. `psycopg2.OperationalError: FATAL: password authentication failed`

**Ошибка:**
```
psycopg2.OperationalError: FATAL: password authentication failed for user "user"
```

**Причина:**
Неправильный пароль

**Решение:**

1. **Проверьте `DATABASE_URL`:**
```env
postgresql://user:PASSWORD@host:port/db
                  ^^^^^^^
```

2. **Railway:**
Используйте `${{Postgres.DATABASE_URL}}` — Railway автоматически подставит правильные креденшалы.

3. **Локально:**
Проверьте PostgreSQL:
```bash
psql -U user -d yovpn
# Введите пароль
```

---

## 🐳 Ошибки Docker

### 1. `COPY failed: no such file or directory`

**Ошибка:**
```
COPY failed: file not found in build context or excluded by .dockerignore: stat package.json: file does not exist
```

**Причина:**
Файл не найден в build context

**Решение:**

1. **Проверьте путь:**
```dockerfile
# Для webapp
WORKDIR /app
COPY webapp/package.json ./  # ✅

# НЕ
COPY package.json ./  # ❌ (если файл в webapp/)
```

2. **Проверьте `.dockerignore`:**
Убедитесь, что файл не исключён.

---

### 2. `denied: permission denied`

**Ошибка:**
```
mkdir: can't create directory '.next': Permission denied
```

**Причина:**
Недостаточно прав

**Решение:**

```dockerfile
# Создайте пользователя
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Дайте права
RUN chown -R nextjs:nodejs /app

# Переключитесь
USER nextjs
```

---

## 🚂 Ошибки Railway

### 1. `Failed to deploy: Service is unhealthy`

**Причина:**
Healthcheck не проходит

**Решение:**

1. **Для API добавьте healthcheck:**
```python
@app.get("/health")
def health():
    return {"status": "healthy"}
```

2. **Railway настройки:**
```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

3. **Для WebApp:**
Railway пингует `/` — убедитесь, что главная страница загружается.

---

### 2. `Build failed: Out of memory`

**Причина:**
Недостаточно RAM

**Решение:**

1. **Оптимизируйте сборку:**
```dockerfile
# Уменьшите memory footprint
ENV NODE_OPTIONS="--max-old-space-size=2048"
```

2. **Используйте .dockerignore:**
Исключите большие файлы.

3. **Upgrade Railway plan:**
Free tier имеет лимит 512MB RAM.

---

## 🌐 Сетевые ошибки

### 1. `ERR_CONNECTION_REFUSED`

**Причина:**
Сервис не запущен или неправильный порт

**Решение:**

1. **Проверьте, что сервис слушает правильный порт:**
```javascript
// WebApp
const port = process.env.PORT || 3000;
app.listen(port);
```

```python
# API
uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
```

2. **Railway:**
Railway автоматически устанавливает `$PORT`.

3. **Bind на 0.0.0.0, не localhost:**
```bash
# ✅ ПРАВИЛЬНО
--host 0.0.0.0

# ❌ НЕПРАВИЛЬНО
--host localhost
```

---

### 2. `WebSocket connection failed`

**Причина:**
WebSocket не поддерживается

**Решение:**

Для Telegram WebApp используйте polling вместо webhook в dev режиме:

```python
# bot/main.py
if os.getenv("ENVIRONMENT") == "development":
    await dp.start_polling(bot)
else:
    await dp.start_webhook(...)
```

---

## 🔍 Дебаггинг

### Общие советы

1. **Проверьте логи:**
```bash
# Railway
Railway Dashboard → Service → Logs

# Docker
docker logs <container_id>

# Локально
tail -f logs/app.log
```

2. **Увеличьте уровень логирования:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. **Тестируйте локально перед деплоем:**
```bash
docker-compose up --build
```

4. **Проверьте переменные окружения:**
```bash
# Railway
Railway Dashboard → Variables

# Локально
cat .env
```

5. **Health checks:**
```bash
# API
curl http://localhost:8000/health

# WebApp
curl http://localhost:3000
```

---

## ✅ Чек-лист перед деплоем

- [ ] Все переменные окружения настроены
- [ ] `next` в `dependencies` (не devDependencies)
- [ ] `output: 'standalone'` в next.config.js
- [ ] Dockerfile использует правильные команды
- [ ] `.dockerignore` создан
- [ ] CORS настроен в API
- [ ] Health check endpoints добавлены
- [ ] DATABASE_URL корректный
- [ ] Локальный build работает
- [ ] Docker build работает
- [ ] Все тесты проходят

---

**Если проблема не решена, откройте [GitHub Issue](https://github.com/yourusername/yovpn/issues) с:**

1. Полным текстом ошибки
2. Логами
3. Версиями (Node, Python, etc.)
4. Шагами для воспроизведения

Мы поможем! 🚀
