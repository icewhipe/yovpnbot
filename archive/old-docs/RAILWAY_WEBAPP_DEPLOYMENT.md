# 🚀 Полное Руководство по Деплою WebApp на Railway

> **Статус**: ✅ Все баги исправлены! WebApp готов к деплою.

Пошаговая инструкция по развертыванию YoVPN WebApp (Next.js 15) на платформе Railway.

---

## 📋 Содержание

1. [Что было исправлено](#что-было-исправлено)
2. [Требования](#требования)
3. [Быстрый старт](#быстрый-старт)
4. [Подробная инструкция](#подробная-инструкция)
5. [Настройка переменных окружения](#настройка-переменных-окружения)
6. [Проверка деплоя](#проверка-деплоя)
7. [Troubleshooting](#troubleshooting)
8. [Мониторинг и обновления](#мониторинг-и-обновления)

---

## ✅ Что было исправлено

### 1. Ошибка `swcMinify` в Next.js 15
**Проблема**: 
```
⚠ Invalid next.config.js options detected: 
⚠ Unrecognized key(s) in object: 'swcMinify'
```

**Решение**: Удалена устаревшая опция `swcMinify` из `next.config.js`, так как в Next.js 15 SWC минификация включена по умолчанию.

**Файл**: `webapp/next.config.js`

### 2. TypeScript ошибка с ref callback
**Проблема**:
```
Type error: Type '(el: HTMLDivElement | null) => HTMLDivElement | null' 
is not assignable to type 'LegacyRef<HTMLDivElement> | undefined'.
```

**Решение**: Исправлен ref callback в `PlatformSelector.tsx` - теперь возвращает `void` вместо значения.

**До**:
```tsx
ref={(el) => (cardsRef.current[index] = el)}
```

**После**:
```tsx
ref={(el) => {
  cardsRef.current[index] = el;
}}
```

**Файл**: `webapp/src/components/PlatformSelector.tsx:129`

### 3. Результат
✅ Сборка проходит успешно  
✅ TypeScript проверки пройдены  
✅ Нет критических ошибок  
✅ Готово к production деплою  

---

## 📦 Требования

### Локальные требования (для разработки)
- Node.js >= 18.0.0
- npm >= 9.0.0
- Git

### Railway аккаунт
- Зарегистрируйтесь на [railway.app](https://railway.app) через GitHub
- Подтвердите email

### Необходимые данные
- **API Backend URL** - URL вашего API сервиса (если уже задеплоен)
- **Telegram Bot Token** - токен от [@BotFather](https://t.me/BotFather)
- (Опционально) Ссылки на скачивание приложений для разных платформ

---

## ⚡ Быстрый старт

Для опытных пользователей - минимальные шаги для деплоя:

```bash
# 1. Клонируйте репозиторий (если еще не сделали)
git clone https://github.com/yourusername/yovpn.git
cd yovpn

# 2. Перейдите на Railway и создайте новый проект
# railway.app/new → Deploy from GitHub repo

# 3. Настройте сервис:
# - Root Directory: webapp
# - Build Command: npm install && npm run build
# - Start Command: npm start

# 4. Добавьте переменные окружения (см. раздел ниже)

# 5. Сгенерируйте домен в Settings → Networking → Generate Domain

# 6. Деплой произойдет автоматически!
```

---

## 📖 Подробная инструкция

### Шаг 1: Подготовка репозитория

#### 1.1 Убедитесь, что у вас последняя версия кода

```bash
git pull origin main
```

#### 1.2 Проверьте структуру проекта

Убедитесь, что у вас есть папка `webapp/` с файлами:
```
webapp/
├── Dockerfile
├── next.config.js
├── package.json
├── src/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   └── types/
└── public/
```

#### 1.3 (Опционально) Проверьте сборку локально

```bash
cd webapp
npm install
npm run build
```

Если сборка успешна - переходите к следующему шагу.

---

### Шаг 2: Создание проекта на Railway

#### 2.1 Войдите в Railway

1. Откройте [railway.app](https://railway.app)
2. Нажмите **"Login"** и войдите через GitHub
3. Разрешите Railway доступ к вашим репозиториям

#### 2.2 Создайте новый проект

1. На главной странице нажмите **"New Project"**
2. Выберите **"Deploy from GitHub repo"**
3. Найдите и выберите ваш репозиторий `yovpn`
4. Нажмите **"Deploy Now"**

Railway создаст первый сервис, но нам нужно его настроить.

#### 2.3 Удалите автоматически созданный сервис (если нужно)

Если Railway создал сервис с неправильными настройками:
1. Кликните на сервис
2. Settings → **Danger Zone** → **Remove Service**

Мы создадим новый с правильными настройками.

---

### Шаг 3: Настройка WebApp сервиса

#### 3.1 Создайте новый сервис

1. В вашем проекте нажмите **"+ New"**
2. Выберите **"GitHub Repo"**
3. Выберите ваш репозиторий
4. Назовите сервис: `webapp` (или `yovpn-webapp`)

#### 3.2 Настройте Root Directory

🔴 **ВАЖНО**: Это критическая настройка!

1. Кликните на сервис `webapp`
2. Перейдите в **Settings**
3. Найдите раздел **"Source"**
4. Установите **Root Directory**: `webapp`

Это указывает Railway работать только с папкой `webapp/`, а не со всем репозиторием.

#### 3.3 Настройте команды сборки

1. В разделе **Settings** → **Deploy**
2. Настройте следующие параметры:

   **Build Command** (опционально, если нужно переопределить):
   ```bash
   npm install && npm run build
   ```

   **Start Command**:
   ```bash
   npm start
   ```

   **Watch Paths** (опционально):
   ```
   webapp/**
   ```

Railway автоматически определит, что это Next.js приложение и использует правильные команды.

#### 3.4 (Рекомендуется) Используйте Dockerfile

Railway автоматически обнаружит `webapp/Dockerfile` и использует его для сборки.

**Преимущества Dockerfile**:
- ✅ Оптимизированная multi-stage сборка
- ✅ Меньший размер образа
- ✅ Standalone режим Next.js (быстрее и легче)
- ✅ Готов к production

Dockerfile уже настроен и находится в `webapp/Dockerfile`. Ничего дополнительно делать не нужно!

---

### Шаг 4: Настройка переменных окружения

#### 4.1 Откройте раздел Variables

1. Кликните на сервис `webapp`
2. Перейдите на вкладку **"Variables"**

#### 4.2 Добавьте обязательные переменные

##### 🔴 Критически важные:

| Переменная | Значение | Описание |
|------------|----------|----------|
| `NODE_ENV` | `production` | Режим работы Node.js |
| `NEXT_PUBLIC_TELEGRAM_BOT_TOKEN` | `ваш_токен_от_botfather` | Токен вашего бота |
| `NEXT_PUBLIC_API_BASE_URL` | `https://api-production-xxxx.up.railway.app` | URL вашего API сервиса |
| `NEXT_PUBLIC_BASE_URL` | `https://webapp-production-yyyy.up.railway.app` | URL WebApp (обновите после генерации домена) |

##### 🟡 Опциональные настройки:

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `NEXT_PUBLIC_DEV_MODE` | `false` | Режим разработки (только для тестирования) |
| `NEXT_TELEMETRY_DISABLED` | `1` | Отключить телеметрию Next.js |

##### 🟢 URL для скачивания приложений (опционально):

```env
NEXT_PUBLIC_ANDROID_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-android.apk
NEXT_PUBLIC_IOS_APP_STORE_URL=https://apps.apple.com/app/v2raytun
NEXT_PUBLIC_MACOS_DMG_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-macos.dmg
NEXT_PUBLIC_WINDOWS_EXE_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-windows.exe
NEXT_PUBLIC_ANDROID_TV_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-tv.apk
```

#### 4.3 Как добавить переменную

1. В разделе **Variables** нажмите **"New Variable"**
2. Введите **Variable Name** (например, `NODE_ENV`)
3. Введите **Variable Value** (например, `production`)
4. Нажмите **"Add"**
5. Повторите для всех переменных

#### 4.4 Пример полного набора переменных

```env
# Node.js
NODE_ENV=production
NEXT_TELEMETRY_DISABLED=1

# Telegram
NEXT_PUBLIC_TELEGRAM_BOT_TOKEN=7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxx

# API Backend (замените на ваш URL)
NEXT_PUBLIC_API_BASE_URL=https://api-production-a1b2c3.up.railway.app

# WebApp URL (обновите после генерации домена в Шаге 5)
NEXT_PUBLIC_BASE_URL=https://webapp-production-d4e5f6.up.railway.app

# Dev Mode
NEXT_PUBLIC_DEV_MODE=false

# Download URLs (опционально)
NEXT_PUBLIC_ANDROID_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-android.apk
NEXT_PUBLIC_IOS_APP_STORE_URL=https://apps.apple.com/app/v2raytun
NEXT_PUBLIC_MACOS_DMG_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-macos.dmg
NEXT_PUBLIC_WINDOWS_EXE_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-windows.exe
NEXT_PUBLIC_ANDROID_TV_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-tv.apk
```

---

### Шаг 5: Генерация публичного URL

#### 5.1 Создайте домен

1. Перейдите в **Settings** → **Networking**
2. Нажмите **"Generate Domain"**
3. Railway автоматически создаст URL вида:
   ```
   https://webapp-production-xxxx.up.railway.app
   ```

#### 5.2 Обновите переменную NEXT_PUBLIC_BASE_URL

🔴 **КРИТИЧЕСКИ ВАЖНО**:

1. Скопируйте сгенерированный URL
2. Вернитесь в **Variables**
3. Найдите переменную `NEXT_PUBLIC_BASE_URL`
4. Обновите её значение на сгенерированный URL
5. Нажмите **"Update"**

Это необходимо для правильной работы Next.js в production режиме.

#### 5.3 (Опционально) Настройте Custom Domain

Если у вас есть собственный домен:

1. Settings → **Networking** → **Custom Domain**
2. Введите ваш домен (например, `app.yourdomain.com`)
3. Railway покажет CNAME запись
4. Добавьте эту запись в DNS вашего домен-провайдера:
   ```
   Type: CNAME
   Name: app
   Value: webapp-production-xxxx.up.railway.app
   TTL: 3600
   ```
5. Дождитесь распространения DNS (5-60 минут)
6. Обновите `NEXT_PUBLIC_BASE_URL` на ваш custom домен

---

### Шаг 6: Деплой!

#### 6.1 Запуск деплоя

После добавления всех переменных окружения:

1. Railway автоматически запустит деплой
2. Или нажмите **"Deploy"** вручную

#### 6.2 Отслеживание прогресса

1. Перейдите на вкладку **"Deployments"**
2. Кликните на активный деплой
3. Откройте **"Build Logs"**

Вы увидите процесс сборки:
```
[builder] Building Dockerfile...
[builder] Stage 1/3: Dependencies
[builder] Stage 2/3: Builder
[builder] npm run build
[builder] ✓ Compiled successfully
[builder] Stage 3/3: Runner
[builder] Build completed successfully
```

#### 6.3 Ожидание завершения

- ⏱️ Первый деплой: ~3-5 минут
- ⏱️ Последующие деплои: ~2-3 минуты

Когда статус изменится на **"Active"** с зеленой галочкой ✅ - деплой завершен!

---

### Шаг 7: Настройка CORS в API

#### 7.1 Зачем это нужно

WebApp будет отправлять запросы к API. Для этого нужно разрешить CORS.

#### 7.2 Настройка API сервиса

1. Откройте сервис `api` в Railway (если он уже задеплоен)
2. Перейдите в **Variables**
3. Найдите или создайте переменную `CORS_ORIGINS`
4. Установите значение - URL вашего WebApp:
   ```
   https://webapp-production-xxxx.up.railway.app
   ```

⚠️ **Важно**: 
- Не добавляйте trailing slash (/)
- Используйте точный URL
- Для нескольких доменов разделяйте запятыми:
  ```
  https://webapp-production-xxxx.up.railway.app,https://app.yourdomain.com
  ```

#### 7.3 Redeploy API

После изменения CORS:
1. Откройте API сервис
2. Deployments → нажмите **три точки** → **Redeploy**

---

### Шаг 8: Настройка Telegram Bot

#### 8.1 Настройка WebApp кнопки в боте

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/mybots`
3. Выберите вашего бота
4. Нажмите **"Bot Settings"** → **"Menu Button"**
5. Выберите **"Configure Menu Button"**
6. Введите URL вашего WebApp:
   ```
   https://webapp-production-xxxx.up.railway.app
   ```
7. Введите текст кнопки (например, "🚀 Запустить приложение")

#### 8.2 (Опционально) Добавьте WEBAPP_URL в бота

Если ваш бот использует переменную `WEBAPP_URL`:

1. Откройте сервис `telegram-bot` в Railway
2. Variables → New Variable
3. Name: `WEBAPP_URL`
4. Value: `https://webapp-production-xxxx.up.railway.app`

---

## 🔍 Проверка деплоя

### Проверка 1: Доступность WebApp

1. Откройте в браузере URL вашего WebApp:
   ```
   https://webapp-production-xxxx.up.railway.app
   ```

2. Вы должны увидеть главную страницу с выбором платформы

### Проверка 2: Console без ошибок

1. Откройте Developer Tools (F12)
2. Перейдите на вкладку **Console**
3. Убедитесь, что нет ошибок (особенно CORS)

### Проверка 3: Работа через Telegram

1. Откройте вашего бота в Telegram
2. Нажмите кнопку Menu (или команду для запуска WebApp)
3. WebApp должен открыться в Telegram
4. Проверьте работу всех функций

### Проверка 4: Логи в Railway

1. Откройте сервис `webapp`
2. Перейдите на вкладку **"Observability"**
3. Проверьте логи на наличие ошибок

Нормальные логи выглядят так:
```
> webapp@1.0.0 start
> next start
▲ Next.js 15.5.6
- Local:        http://localhost:3000
- Network:      http://0.0.0.0:3000

✓ Ready in 234ms
```

### Проверка 5: Метрики

1. В разделе **"Observability"** → **"Metrics"**
2. Проверьте:
   - CPU usage: должен быть < 50% в idle
   - Memory usage: должен быть < 300MB в idle
   - HTTP requests: должны быть успешные (200, 304)

---

## 🔧 Настройка переменных окружения

### Полный список переменных

#### Обязательные

```env
# Production Mode
NODE_ENV=production

# Telegram Bot Token
NEXT_PUBLIC_TELEGRAM_BOT_TOKEN=your_bot_token_here

# API Backend URL
NEXT_PUBLIC_API_BASE_URL=https://your-api-url.railway.app

# WebApp Public URL (обновите после генерации домена)
NEXT_PUBLIC_BASE_URL=https://your-webapp-url.railway.app
```

#### Рекомендуемые

```env
# Disable Next.js Telemetry
NEXT_TELEMETRY_DISABLED=1

# Dev Mode (false для production)
NEXT_PUBLIC_DEV_MODE=false
```

#### Опциональные (ссылки на скачивание)

```env
# Android APK
NEXT_PUBLIC_ANDROID_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-android.apk

# iOS App Store
NEXT_PUBLIC_IOS_APP_STORE_URL=https://apps.apple.com/app/v2raytun

# macOS DMG
NEXT_PUBLIC_MACOS_DMG_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-macos.dmg

# Windows EXE
NEXT_PUBLIC_WINDOWS_EXE_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-windows.exe

# Android TV APK
NEXT_PUBLIC_ANDROID_TV_APK_URL=https://github.com/yovpn/v2raytun/releases/latest/download/v2raytun-tv.apk
```

### Как получить значения

#### NEXT_PUBLIC_TELEGRAM_BOT_TOKEN

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/mybots`
3. Выберите вашего бота
4. Нажмите **"API Token"**
5. Скопируйте токен

#### NEXT_PUBLIC_API_BASE_URL

1. Откройте Railway проект
2. Перейдите к сервису `api`
3. Settings → Networking
4. Скопируйте сгенерированный домен

#### NEXT_PUBLIC_BASE_URL

1. Откройте Railway проект
2. Перейдите к сервису `webapp`
3. Settings → Networking → Generate Domain
4. Скопируйте сгенерированный домен

---

## 🐛 Troubleshooting

### Проблема 1: Build Failed - "Invalid next.config.js"

**Симптомы**:
```
⚠ Invalid next.config.js options detected
⚠ Unrecognized key(s) in object: 'swcMinify'
```

**Решение**: ✅ Уже исправлено! Убедитесь, что используете последнюю версию кода.

### Проблема 2: Build Failed - TypeScript error

**Симптомы**:
```
Type error in PlatformSelector.tsx
```

**Решение**: ✅ Уже исправлено! Обновите код из репозитория.

### Проблема 3: WebApp не загружается (белый экран)

**Возможные причины**:
1. Неправильные переменные окружения
2. CORS ошибки

**Решение**:
1. Проверьте Browser Console (F12)
2. Убедитесь, что все `NEXT_PUBLIC_*` переменные установлены
3. Проверьте `NEXT_PUBLIC_API_BASE_URL` - должен быть доступен
4. Проверьте CORS в API сервисе

### Проблема 4: CORS ошибки

**Симптомы** в Console:
```
Access to fetch at 'https://api...' from origin 'https://webapp...' 
has been blocked by CORS policy
```

**Решение**:
1. Откройте API сервис в Railway
2. Переменная `CORS_ORIGINS` должна содержать URL WebApp
3. Формат: `https://webapp-production-xxxx.up.railway.app` (без trailing slash)
4. Redeploy API сервиса

### Проблема 5: 404 Not Found

**Симптомы**: WebApp показывает 404 при переходе по URL

**Возможные причины**:
1. Деплой еще не завершен
2. Сервис не запущен

**Решение**:
1. Проверьте статус деплоя: должен быть "Active" ✅
2. Проверьте логи на ошибки
3. Попробуйте Redeploy

### Проблема 6: Out of Memory

**Симптомы**:
```
JavaScript heap out of memory
```

**Решение**:
1. Railway Hobby план: 512MB RAM (может быть недостаточно)
2. Решения:
   - Используйте Dockerfile (уже настроен, использует standalone режим)
   - Upgrade до Developer плана ($5/мес, 8GB RAM)
   - Оптимизируйте изображения

### Проблема 7: Медленная загрузка

**Решение**:
1. Используйте Dockerfile (standalone режим Next.js быстрее)
2. Включите CDN (Railway Pro)
3. Оптимизируйте изображения в `/public`

### Проблема 8: WebApp работает, но не открывается в Telegram

**Решение**:
1. Проверьте URL в BotFather (должен быть `https://`)
2. Убедитесь, что WebApp доступен из браузера
3. Telegram требует HTTPS (Railway предоставляет автоматически)
4. Проверьте, что домен не в черном списке Telegram

### Проблема 9: Переменные окружения не применяются

**Симптомы**: Изменения переменных не отражаются

**Решение**:
1. После изменения переменных нужен **Redeploy**
2. Deployments → три точки → Redeploy
3. Переменные с `NEXT_PUBLIC_*` встраиваются в билд (нужна пересборка)

### Проблема 10: Railway показывает "Deployment Failed"

**Решение**:
1. Откройте Deployments → кликните на failed deployment
2. Проверьте Build Logs на ошибки
3. Частые причины:
   - Отсутствует `package.json`
   - Неправильный Root Directory (должен быть `webapp`)
   - Syntax ошибки в коде
   - Отсутствуют зависимости

---

## 📊 Мониторинг и обновления

### Мониторинг в Railway

#### 1. Логи в реальном времени

1. Сервис `webapp` → **Observability**
2. Логи обновляются автоматически
3. Фильтруйте по уровню: Info, Warning, Error

#### 2. Метрики

1. **Observability** → **Metrics**
2. Отслеживайте:
   - CPU Usage
   - Memory Usage
   - Network Bandwidth
   - HTTP Requests

#### 3. Алерты

Railway автоматически отправляет алерты:
- Когда деплой завершен
- Когда произошла ошибка
- Когда сервис перезапустился

Настройте получение алертов:
1. Account Settings → Notifications
2. Выберите способ уведомлений (Email, Slack, Discord)

### Внешний мониторинг

#### UptimeRobot (бесплатно)

1. Зарегистрируйтесь на [uptimerobot.com](https://uptimerobot.com)
2. Add New Monitor:
   - Type: HTTP(s)
   - URL: `https://your-webapp.railway.app`
   - Interval: 5 minutes
3. Получайте алерты при недоступности

#### BetterStack (рекомендуется)

1. [betterstack.com](https://betterstack.com)
2. Более продвинутый мониторинг
3. Бесплатный план: 3 monitors

### Обновление приложения

#### Автоматический деплой (рекомендуется)

Railway автоматически деплоит при push в GitHub:

1. Внесите изменения в код
2. Commit и push:
   ```bash
   git add .
   git commit -m "Update webapp"
   git push origin main
   ```
3. Railway автоматически обнаружит изменения
4. Начнется новый деплой (~2-3 минуты)

#### Ручной деплой

1. Откройте сервис `webapp`
2. Deployments → три точки → **Redeploy**
3. Выберите нужный commit (или latest)

#### Откат к предыдущей версии

1. Deployments → найдите успешный деплой
2. Три точки → **Redeploy**
3. Railway откатит на выбранную версию

### Zero-Downtime Deployments

Railway использует rolling deployments:
- ✅ Новая версия деплоится параллельно
- ✅ Трафик переключается только после успешного запуска
- ✅ Старая версия продолжает работать до готовности новой

### Просмотр предыдущих деплоев

1. Deployments
2. История всех деплоев с:
   - Commit message
   - Дата и время
   - Статус (Success/Failed)
   - Build logs
   - Duration

---

## 💰 Стоимость и оптимизация

### Railway Pricing

#### Hobby Plan (Бесплатно)
- ✅ $5 кредитов в месяц
- ✅ 512MB RAM на сервис
- ✅ 1GB Disk
- ✅ Shared CPU
- ⚠️ Сервисы засыпают при неактивности (5 минут)

**Достаточно для**: Тестирования, малого трафика (<1000 пользователей/день)

#### Developer Plan ($5/месяц)
- ✅ $5 кредитов включено + pay as you go
- ✅ 8GB RAM на сервис
- ✅ 100GB Disk
- ✅ Priority CPU
- ✅ Сервисы всегда активны

**Рекомендуется для**: Production, средний трафик

### Оптимизация расходов

#### 1. Используйте Dockerfile
✅ Уже настроен в проекте!

Преимущества:
- Меньший размер образа (~150MB вместо ~800MB)
- Быстрее деплой
- Меньше CPU/RAM использование

#### 2. Оптимизируйте изображения

В `/public`:
- Используйте WebP формат
- Сжимайте изображения
- Используйте правильные размеры

#### 3. Настройте кэширование

Next.js автоматически кэширует статику. Убедитесь, что:
```js
// next.config.js
output: 'standalone', // ✅ Уже настроено
```

#### 4. Мониторьте использование

1. Observability → Metrics
2. Следите за:
   - Memory usage (если >400MB - оптимизируйте)
   - CPU usage (если >80% - масштабируйте)

### Примерная стоимость

**Hobby Plan (Free tier)**:
- WebApp only: ~$0-2/месяц (в рамках $5 кредитов)

**Developer Plan**:
- WebApp + API + Bot + Redis: ~$5-10/месяц

---

## 📚 Дополнительные ресурсы

### Документация

- [Railway Documentation](https://docs.railway.app/)
- [Next.js 15 Documentation](https://nextjs.org/docs)
- [Telegram WebApps](https://core.telegram.org/bots/webapps)

### Полезные команды

#### Проверка переменных окружения локально

```bash
cd webapp
cat .env.local
```

#### Тестирование production сборки локально

```bash
cd webapp
npm run build
npm start
```

Откройте: http://localhost:3000

#### Проверка размера сборки

```bash
cd webapp
npm run build
# Смотрите размер в выводе
```

### Поддержка

Если возникли проблемы:

1. ✅ Проверьте этот гайд и раздел Troubleshooting
2. 📋 Проверьте логи в Railway (Observability → Logs)
3. 🔍 Проверьте Browser Console (F12)
4. 💬 Создайте Issue на GitHub
5. 📧 Свяжитесь с поддержкой Railway

---

## ✅ Чеклист перед запуском

Перед тем как запустить в production, убедитесь:

### Код и конфигурация
- [ ] Последняя версия кода из репозитория
- [ ] `next.config.js` не содержит `swcMinify`
- [ ] TypeScript ошибки исправлены
- [ ] Локальная сборка успешна (`npm run build`)

### Railway настройки
- [ ] Root Directory установлен: `webapp`
- [ ] Dockerfile обнаружен и используется
- [ ] Все обязательные переменные окружения добавлены
- [ ] Публичный домен сгенерирован
- [ ] `NEXT_PUBLIC_BASE_URL` обновлен с правильным URL

### API и интеграции
- [ ] API сервис задеплоен и доступен
- [ ] `CORS_ORIGINS` в API содержит URL WebApp
- [ ] Telegram Bot Token валиден
- [ ] Menu Button настроен в BotFather

### Проверка работоспособности
- [ ] WebApp открывается в браузере
- [ ] WebApp открывается через Telegram
- [ ] Нет CORS ошибок в Console
- [ ] Логи в Railway без критических ошибок
- [ ] Метрики в норме (CPU <50%, Memory <300MB)

### Мониторинг (опционально, но рекомендуется)
- [ ] Настроен UptimeRobot или аналог
- [ ] Настроены алерты в Railway
- [ ] Добавлен error tracking (Sentry или аналог)

---

## 🎉 Готово!

Поздравляем! Ваш YoVPN WebApp теперь задеплоен на Railway и готов к использованию.

### Следующие шаги:

1. 📱 Протестируйте WebApp через Telegram
2. 👥 Пригласите первых пользователей
3. 📊 Настройте мониторинг
4. 🚀 Масштабируйте при необходимости

---

## 📝 Краткая инструкция (TL;DR)

Для опытных пользователей - минимум шагов:

```bash
# 1. Railway: New Project → Deploy from GitHub
# 2. Настройки сервиса:
#    - Name: webapp
#    - Root Directory: webapp
#    - Start Command: npm start
# 3. Переменные окружения:
NODE_ENV=production
NEXT_PUBLIC_TELEGRAM_BOT_TOKEN=your_token
NEXT_PUBLIC_API_BASE_URL=https://your-api.railway.app
NEXT_PUBLIC_BASE_URL=https://your-webapp.railway.app
# 4. Settings → Networking → Generate Domain
# 5. Обновить NEXT_PUBLIC_BASE_URL с новым доменом
# 6. API: добавить CORS_ORIGINS с URL WebApp
# 7. BotFather: настроить Menu Button с URL WebApp
# ✅ Готово!
```

**Время деплоя**: ~10-15 минут  
**Первый деплой**: ~3-5 минут  

---

**Успешного деплоя! 🚀**

_Последнее обновление: 2025-10-21_
