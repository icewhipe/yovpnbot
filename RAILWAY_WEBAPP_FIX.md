# Исправление ошибки "sh: next: not found" на Railway

## 🔍 Проблема

При деплое webapp на Railway возникает ошибка:
```
sh: next: not found
> yovpn-webapp@1.0.0 start
> next start
sh: next: not found
```

Это происходит потому, что Railway пытается запустить `npm start` БЕЗ предварительной установки зависимостей и сборки приложения.

## ✅ Решение

### Вариант 1: Использовать nixpacks.toml (Рекомендуется для Railway)

Я создал файл `webapp/nixpacks.toml`, который правильно настраивает процесс сборки:

1. **Установка зависимостей**: `npm ci --include=dev`
2. **Сборка приложения**: `npm run build`
3. **Запуск приложения**: `npm start`

Этот файл уже создан в проекте!

### Вариант 2: Использовать Dockerfile (Альтернатива)

Если хотите использовать Dockerfile вместо Nixpacks:

1. Зайдите в настройки сервиса webapp на Railway
2. Перейдите в **Settings** → **Deploy**
3. Найдите **Build Settings**
4. Установите:
   - **Builder**: `Dockerfile`
   - **Dockerfile Path**: `webapp/Dockerfile`
5. Сохраните изменения

## 🚀 Инструкция по деплою

### Шаг 1: Обновите код на Railway

Если вы используете GitHub:
```bash
git add .
git commit -m "Fix webapp nixpacks configuration"
git push
```

Railway автоматически запустит новый деплой.

### Шаг 2: Проверьте переменные окружения

Убедитесь, что в настройках webapp на Railway добавлены все необходимые переменные:

```bash
# Обязательные переменные
TELEGRAM_BOT_TOKEN="8385845645:AAGiZhSwkRgndegtTsy573Smnul2wFNwLu0"
MARZBAN_API_URL="https://ваш-marzban-сервер.com/api"
MARZBAN_ADMIN_TOKEN="ваш_токен"

# Next.js переменные
NODE_ENV="production"
NEXT_PUBLIC_TELEGRAM_BOT_TOKEN="8385845645:AAGiZhSwkRgndegtTsy573Smnul2wFNwLu0"
NEXT_PUBLIC_API_BASE_URL="https://api-production-8ffe.up.railway.app"
NEXT_PUBLIC_BASE_URL="https://webapp-production-5fe6.up.railway.app"
NEXT_PUBLIC_DEV_MODE="false"

# Download URLs
NEXT_PUBLIC_ANDROID_APK_URL="https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-android.apk"
NEXT_PUBLIC_IOS_APP_STORE_URL="https://apps.apple.com/app/v2raytun"
NEXT_PUBLIC_MACOS_DMG_URL="https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-macos.dmg"
NEXT_PUBLIC_WINDOWS_EXE_URL="https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-windows.exe"
NEXT_PUBLIC_ANDROID_TV_APK_URL="https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-tv.apk"
```

### Шаг 3: Проверьте логи деплоя

После пуша на GitHub:

1. Откройте Railway Dashboard
2. Перейдите в сервис **webapp**
3. Откройте **Deployments** → последний деплой
4. Проверьте логи сборки:

**Правильный вывод должен быть:**
```
[nixpacks] Installing dependencies...
npm ci --include=dev
...
[nixpacks] Building application...
npm run build
...
Route (app)                              Size     First Load JS
┌ ○ /                                    ...
...
[nixpacks] Starting application...
npm start
> yovpn-webapp@1.0.0 start
> next start
✓ Ready in XXXms
```

**НЕ должно быть:**
```
sh: next: not found
```

### Шаг 4: Настройки Railway для webapp

Убедитесь, что в настройках сервиса webapp:

1. **Root Directory**: `webapp` (или оставьте пустым, если nixpacks.toml в корне webapp)
2. **Watch Paths**: `webapp/**` (чтобы деплой запускался только при изменениях webapp)
3. **Start Command**: оставьте пустым (nixpacks использует команду из файла)

## 🔧 Важные исправления

### 1. Файл `webapp/nixpacks.toml` (создан)

```toml
[phases.setup]
nixPkgs = ["nodejs-18_x", "npm-9_x"]

[phases.install]
cmds = ["npm ci --include=dev"]

[phases.build]
cmds = ["npm run build"]

[start]
cmd = "npm start"

[variables]
NODE_ENV = "production"
NEXT_TELEMETRY_DISABLED = "1"
```

### 2. Файл `webapp/next.config.js` (исправлен)

Убран `assetPrefix`, который вызывал проблемы с относительными путями на Railway.

### 3. Переменные окружения

Добавлена критически важная переменная `MARZBAN_API_URL`, которая отсутствовала.

## ⚠️ Частые проблемы

### Проблема: next: not found

**Причина**: Railway не установил зависимости перед запуском

**Решение**: 
- Убедитесь, что файл `webapp/nixpacks.toml` существует
- Проверьте, что Railway использует правильный Root Directory

### Проблема: Build failed

**Причина**: Ошибки в коде или отсутствующие переменные окружения

**Решение**:
- Проверьте логи сборки
- Убедитесь, что все `NEXT_PUBLIC_*` переменные добавлены ПЕРЕД сборкой

### Проблема: Application Error после деплоя

**Причина**: Отсутствуют runtime переменные или неправильный порт

**Решение**:
- Railway автоматически устанавливает `PORT` переменную
- Next.js по умолчанию использует порт 3000
- Убедитесь, что переменные `NEXT_PUBLIC_API_BASE_URL` и `NEXT_PUBLIC_BASE_URL` правильные

## 📝 Чек-лист деплоя webapp

- [ ] Файл `webapp/nixpacks.toml` создан и закоммичен
- [ ] Все переменные окружения добавлены на Railway
- [ ] Переменная `MARZBAN_API_URL` установлена (критично!)
- [ ] URL в `NEXT_PUBLIC_API_BASE_URL` и `NEXT_PUBLIC_BASE_URL` начинаются с `https://`
- [ ] Root Directory установлен на `webapp` (или пусто)
- [ ] Код запушен в GitHub
- [ ] Railway запустил новый деплой
- [ ] Логи показывают успешную сборку без ошибок
- [ ] Webapp открывается по URL от Railway

## 🎯 Проверка после деплоя

1. Откройте URL webapp (например, `https://webapp-production-5fe6.up.railway.app`)
2. Вы должны увидеть интерфейс webapp
3. Проверьте консоль браузера (F12) на наличие ошибок
4. Убедитесь, что API запросы идут на правильный API сервер

## 🆘 Если всё равно не работает

1. **Проверьте логи сборки** на Railway
2. **Проверьте runtime логи** в разделе Deployments
3. **Убедитесь, что используется Node.js 18+**
4. **Попробуйте Redeploy** (кнопка в Railway)
5. **Очистите кэш сборки**: Settings → Clear Cache → Deploy

## 📞 Дополнительная помощь

Если проблема не решена:
- Скопируйте полные логи сборки и runtime
- Проверьте версию Node.js: должна быть 18.x
- Убедитесь, что package.json содержит все зависимости
- Проверьте, что package-lock.json закоммичен в репозиторий
