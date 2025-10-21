# Настройка активации подписки с Marzban API

## 🎯 Обзор

Теперь когда пользователь нажимает кнопку "Активировать подписку" в webapp, система **автоматически создает или обновляет пользователя в Marzban**.

## 🔧 Что было исправлено

### Проблема
Раньше при нажатии "Активировать подписку" ничего не происходило в Marzban API - просто логировалась активация без реального создания пользователя.

### Решение
Добавлен полный цикл активации:

1. **Новый API эндпоинт**: `POST /api/subscription/activate`
2. **Создание/обновление пользователя в Marzban** при активации
3. **Возврат реального subscription URI** из Marzban
4. **Автоматическое копирование и открытие** в приложении

## 📝 Настройка

### 1. Переменные окружения для API

Добавьте в `/workspace/api/.env`:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
SECRET_KEY=your_secret_key_here

# Marzban API
MARZBAN_API_URL=https://your-marzban-domain.com/api
MARZBAN_ADMIN_TOKEN=your_marzban_admin_token

# Download URLs
ANDROID_APK_URL=https://github.com/2dust/v2rayNG/releases/latest
IOS_APP_STORE_URL=https://apps.apple.com/app/shadowrocket/id932747118
MACOS_DMG_URL=https://github.com/v2rayA/v2rayA/releases/latest
WINDOWS_EXE_URL=https://github.com/2dust/v2rayN/releases/latest
ANDROID_TV_APK_URL=https://github.com/2dust/v2rayNG/releases/latest
```

### 2. Получение Marzban Admin Token

#### Вариант A: Через Marzban UI (рекомендуется)
1. Откройте Marzban админ-панель
2. Войдите как администратор
3. Перейдите в **Settings** → **API Tokens**
4. Создайте новый API Token или скопируйте существующий
5. Скопируйте токен в `MARZBAN_ADMIN_TOKEN`

#### Вариант B: Через API (если нет UI)
```bash
curl -X POST "https://your-marzban-domain.com/api/admin/token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_admin_password"
  }'
```

Ответ будет содержать `access_token` - это ваш `MARZBAN_ADMIN_TOKEN`.

### 3. Переменные окружения для бота

Добавьте в `/workspace/.env`:

```bash
# Marzban (для бота)
MARZBAN_API_URL=https://your-marzban-domain.com/api
MARZBAN_ADMIN_TOKEN=your_marzban_admin_token
```

## 🚀 Как работает активация

### Поток активации

```
Пользователь → WebApp → Нажимает "Активировать"
                    ↓
              API endpoint: /api/subscription/activate
                    ↓
              Проверяет существует ли пользователь в Marzban
                    ↓
        ┌─────────────────────────────┐
        ↓                             ↓
   Существует                   Не существует
        ↓                             ↓
   Обновляет подписку          Создает нового пользователя
   (+30 дней)                  (30 дней, безлимитный трафик)
        ↓                             ↓
        └──────────────┬──────────────┘
                       ↓
              Возвращает subscription_uri
                       ↓
              WebApp копирует URI
                       ↓
              Открывает приложение v2raytun
                       ↓
              ✅ Успешная активация!
```

### Создаваемый пользователь

При активации создается пользователь со следующими параметрами:

```json
{
  "username": "user_123456789" или "@telegram_username",
  "expire": 2592000,  // +30 дней от текущей даты (в секундах)
  "data_limit": 0,    // Безлимитный трафик
  "status": "active",
  "proxies": {
    "vless": {
      "id": "uuid-v4",
      "flow": "xtls-rprx-vision"
    }
  }
}
```

## 🧪 Тестирование

### 1. Запустите API

```bash
cd /workspace/api
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Проверьте логи при запуске:
```
🚀 Starting YoVPN WebApp API...
📡 Marzban API URL: https://your-marzban-domain.com/api
✅ Marzban API is available and ready
```

Если видите `⚠️ Marzban API is not available` - проверьте:
- Правильность `MARZBAN_API_URL`
- Доступность Marzban сервера
- Корректность `MARZBAN_ADMIN_TOKEN`

### 2. Протестируйте эндпоинт

```bash
# Тест активации подписки
curl -X POST "http://localhost:8000/api/subscription/activate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123456789,
    "platform": "android",
    "telegram_username": "testuser"
  }'
```

Успешный ответ:
```json
{
  "success": true,
  "message": "Subscription created successfully",
  "subscription_uri": "https://your-marzban.com/sub/testuser",
  "expires_at": "2025-11-20T12:00:00",
  "marzban_username": "testuser"
}
```

### 3. Проверьте в Marzban UI

1. Откройте Marzban админ-панель
2. Перейдите в **Users**
3. Найдите созданного пользователя (`testuser` или `user_123456789`)
4. Проверьте:
   - ✅ Status: Active
   - ✅ Expire: +30 дней
   - ✅ Data Limit: Unlimited (0 или ∞)
   - ✅ Subscription URL создан

## 🔍 Отладка

### Логи API

```bash
# Смотреть логи в реальном времени
tail -f /workspace/api/logs/api.log

# Или если запущено через uvicorn
# Логи будут в консоли
```

Важные логи:
```
🔄 Activating subscription for user 123456789 (marzban: testuser)
🆕 Creating new user testuser in Marzban...
✅ MarzbanService initialized
```

### Проблемы и решения

#### ❌ "Marzban API недоступен"
**Проблема**: Не удается подключиться к Marzban

**Решение**:
1. Проверьте `MARZBAN_API_URL` - должен заканчиваться на `/api`
2. Убедитесь, что Marzban доступен: `curl https://your-marzban.com/api/system`
3. Проверьте файрвол и сетевые настройки

#### ❌ "Invalid Telegram data"
**Проблема**: Ошибка валидации Telegram WebApp init data

**Решение**:
1. Убедитесь, что `TELEGRAM_BOT_TOKEN` в `/workspace/api/.env` правильный
2. Проверьте, что WebApp запущен через Telegram (не в обычном браузере)

#### ❌ "Failed to create user in Marzban"
**Проблема**: Ошибка при создании пользователя

**Решение**:
1. Проверьте `MARZBAN_ADMIN_TOKEN` - должен быть валидным
2. Убедитесь, что у токена есть права на создание пользователей
3. Проверьте логи Marzban на ошибки

#### ❌ Mock data возвращается вместо реальных данных
**Проблема**: API возвращает `v2ray://mock-subscription-...`

**Решение**:
1. Проверьте, что MarzbanService успешно инициализирован
2. Смотрите логи при запуске API:
   ```
   ✅ Successfully imported bot services
   🔧 Initializing MarzbanService with URL: ...
   ✅ MarzbanService initialized
   ```
3. Если видите `⚠️ Failed to import bot services` - проверьте зависимости

## 📱 Использование в WebApp

После настройки пользователи смогут:

1. **Выбрать платформу** (Android, iOS, macOS, Windows, Android TV)
2. **Скачать приложение** v2raytun
3. **Нажать "Активировать подписку"**
   - ✅ Автоматически создается пользователь в Marzban
   - ✅ Subscription URI копируется в буфер обмена
   - ✅ Открывается приложение v2raytun с URI
   - ✅ Подписка активируется в 1 клик!

## 🎉 Готово!

Теперь активация подписки работает полностью автоматически с реальным созданием пользователей в Marzban!

## 📚 API Документация

После запуска API документация доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Основные эндпоинты:
- `POST /api/subscription/activate` - Активация подписки (создает/обновляет пользователя)
- `GET /api/subscription/{user_id}` - Получить данные подписки
- `POST /api/track/activation` - Трекинг активации (аналитика)
- `GET /api/health` - Проверка здоровья API
