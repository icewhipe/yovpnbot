# 🚀 Быстрое исправление ошибки Railway

## ❌ Текущие ошибки

### 1. Webapp: `sh: next: not found`
Railway пытается запустить webapp БЕЗ установки зависимостей

### 2. Bot: `⚠️ Marzban API URL не настроен`
Неправильное название переменных окружения

## ✅ Решение

### Шаг 1: Обновите код (commitтю изменения)

```bash
git add .
git commit -m "Fix Railway deployment configuration"
git push origin main
```

### Шаг 2: Исправьте переменные окружения на Railway

#### Сервис: telegram-bot (Бот)

**Добавьте/Исправьте:**
```bash
TELEGRAM_BOT_TOKEN="8385845645:AAGiZhSwkRgndegtTsy573Smnul2wFNwLu0"
MARZBAN_API_URL="https://ваш-marzban-сервер.com/api"
MARZBAN_ADMIN_TOKEN="ваш_новый_токен_не_истекший"
SECRET_KEY="минимум-32-символа-случайная-строка"
```

**Удалите (если есть):**
- `USERBOT_TOKEN` (используйте `TELEGRAM_BOT_TOKEN` вместо этого)

#### Сервис: webapp (Веб-приложение)

**Добавьте/Исправьте:**
```bash
# КРИТИЧНО - добавьте эту переменную!
MARZBAN_API_URL="https://ваш-marzban-сервер.com/api"

# Исправьте URL (добавьте https://)
NEXT_PUBLIC_API_BASE_URL="https://api-production-8ffe.up.railway.app"
NEXT_PUBLIC_BASE_URL="https://webapp-production-5fe6.up.railway.app"

# Остальные переменные
TELEGRAM_BOT_TOKEN="8385845645:AAGiZhSwkRgndegtTsy573Smnul2wFNwLu0"
MARZBAN_ADMIN_TOKEN="ваш_токен"
NODE_ENV="production"
NEXT_PUBLIC_TELEGRAM_BOT_TOKEN="8385845645:AAGiZhSwkRgndegtTsy573Smnul2wFNwLu0"
NEXT_PUBLIC_DEV_MODE="false"
```

#### Сервис: api (API сервер)

**Добавьте/Исправьте:**
```bash
TELEGRAM_BOT_TOKEN="8385845645:AAGiZhSwkRgndegtTsy573Smnul2wFNwLu0"
MARZBAN_API_URL="https://ваш-marzban-сервер.com/api"
MARZBAN_ADMIN_TOKEN="ваш_токен"
SECRET_KEY="тот-же-ключ-что-и-в-боте"
```

### Шаг 3: Получите новый Marzban токен

**Ваш текущий токен истёк!** (exp: 1761066994 = 21 октября 2024)

1. Откройте панель Marzban
2. Войдите как admin
3. Перейдите в настройки профиля
4. Сгенерируйте новый API токен
5. Скопируйте его
6. Вставьте во ВСЕ три сервиса на Railway как `MARZBAN_ADMIN_TOKEN`

### Шаг 4: Настройки Railway

#### Для webapp:
1. Зайдите в Settings сервиса webapp
2. В разделе **Deploy**:
   - **Root Directory**: `webapp`
   - **Watch Paths**: `webapp/**`
3. В разделе **Networking**:
   - Убедитесь, что домен сгенерирован
4. Сохраните

#### Для bot:
1. Зайдите в Settings сервиса bot
2. В разделе **Deploy**:
   - **Root Directory**: оставьте пустым
   - **Start Command**: `python bot/main.py`
3. Сохраните

#### Для api:
1. Зайдите в Settings сервиса api
2. В разделе **Deploy**:
   - **Root Directory**: `api`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Сохраните

### Шаг 5: Redeploy всех сервисов

После обновления переменных:

1. Откройте каждый сервис
2. Нажмите **Deployments**
3. Нажмите три точки (⋮) справа от последнего деплоя
4. Выберите **Redeploy**

Или просто сделайте:
```bash
git commit --allow-empty -m "Trigger redeploy"
git push
```

## 🔍 Проверка после деплоя

### Bot должен показать:
```
✅ MarzbanService инициализирован: https://ваш-сервер.com/api
✅ Marzban API доступен
🚀 Запуск YoVPN Bot...
✓ Ready to handle updates
```

### Webapp должен показать:
```
[nixpacks] Installing dependencies...
[nixpacks] Building application...
Route (app)                              Size     First Load JS
✓ Compiled successfully
[nixpacks] Starting application...
✓ Ready in XXXms
```

### API должен показать:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

## ⚠️ Важно!

1. **MARZBAN_API_URL** должен быть ПОЛНЫМ URL с `https://`
2. **Токен Marzban** должен быть ДЕЙСТВИТЕЛЬНЫМ (не истекшим)
3. **Все URL** в переменных должны начинаться с `https://`
4. **SECRET_KEY** должен быть одинаковым во всех сервисах

## 🎯 Краткий чеклист

- [ ] Код закоммичен и запушен в GitHub
- [ ] Добавлена переменная `MARZBAN_API_URL` во ВСЕ сервисы
- [ ] Исправлены URL (добавлен `https://`)
- [ ] Получен и добавлен НОВЫЙ токен Marzban (старый истёк!)
- [ ] Переименована `USERBOT_TOKEN` → `TELEGRAM_BOT_TOKEN`
- [ ] Настроены Root Directory для каждого сервиса
- [ ] Выполнен Redeploy всех сервисов
- [ ] Проверены логи - нет ошибок
- [ ] Bot отвечает в Telegram
- [ ] Webapp открывается в браузере
- [ ] API отвечает на запросы

## 📞 Если не работает

Проверьте логи каждого сервиса:
1. Railway Dashboard → Сервис → Deployments → View Logs
2. Ищите конкретные ошибки
3. Убедитесь, что Marzban сервер доступен из интернета

Попробуйте открыть ваш `MARZBAN_API_URL` в браузере - должен открываться.
