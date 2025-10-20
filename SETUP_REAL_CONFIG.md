# Настройка реальной конфигурации YOVPN Bot

## 🔧 Текущая проблема

Бот запускается, но не может подключиться к Marzban API, потому что используются тестовые значения:

```
API URL: https://test.com/api
Admin Token: test_token...
```

## ✅ Решение

### 1. Настройте реальные значения в .env файле

```bash
# Отредактируйте .env файл
nano .env
```

### 2. Замените тестовые значения на реальные

```env
# Telegram Bot Configuration
USERBOT_TOKEN=your_actual_telegram_bot_token_here

# Marzban API Configuration
MARZBAN_API_URL=https://your-actual-marzban-domain.com/api
MARZBAN_ADMIN_TOKEN=your_actual_marzban_admin_token_here

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=marzban
DB_USER=marzban
DB_PASSWORD=your_secure_database_password_here

# Data file path (relative to project root)
DATA_FILE=data.json
```

### 3. Как получить реальные значения

#### Telegram Bot Token:
1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен вида: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

#### Marzban API URL:
1. Это URL вашего Marzban сервера
2. Обычно: `https://your-domain.com/api`
3. Или: `https://your-ip:port/api`

#### Marzban Admin Token:
1. Войдите в панель Marzban
2. Перейдите в Settings → API
3. Скопируйте Admin Token

### 4. Проверьте подключение

После настройки реальных значений запустите тест:

```bash
python3 test_marzban.py
```

Если все настроено правильно, вы увидите:
```
✅ Marzban API доступен!
✅ Системная информация получена:
   Версия: 1.0.0
   Статус: running
```

### 5. Запустите бота

```bash
python3 main_improved.py
```

## 🚨 Важные замечания

### Безопасность:
- **НЕ ДЕЛИТЕСЬ** токенами и паролями
- **НЕ КОММИТЬТЕ** .env файл в Git
- **ИСПОЛЬЗУЙТЕ** сильные пароли

### SSL сертификаты:
- Убедитесь, что Marzban использует валидный SSL сертификат
- Если используется самоподписанный сертификат, может потребоваться дополнительная настройка

### Сеть:
- Убедитесь, что VPS может подключиться к Marzban серверу
- Проверьте файрвол и сетевые настройки

## 🔍 Диагностика проблем

### Проблема: "Ошибка соединения"
**Возможные причины:**
- Неправильный URL API
- Marzban сервер не запущен
- Проблемы с сетью
- Блокировка файрволом

**Решение:**
```bash
# Проверьте доступность сервера
curl -I https://your-marzban-domain.com/api/system

# Проверьте с VPS
ping your-marzban-domain.com
```

### Проблема: "Ошибка авторизации"
**Возможные причины:**
- Неправильный токен
- Токен истек
- Неправильные права доступа

**Решение:**
- Проверьте токен в панели Marzban
- Создайте новый токен
- Убедитесь, что у токена есть права администратора

### Проблема: "SSL ошибка"
**Возможные причины:**
- Самоподписанный сертификат
- Неправильный домен
- Истекший сертификат

**Решение:**
- Используйте валидный SSL сертификат
- Или временно отключите SSL проверку (НЕ РЕКОМЕНДУЕТСЯ)

## 📞 Поддержка

Если проблемы продолжаются:
1. Проверьте логи: `tail -f bot.log`
2. Запустите тест: `python3 test_marzban.py`
3. Проверьте конфигурацию: `cat .env`
4. Обратитесь к документации Marzban