# 🚀 Инструкция по настройке YoVPN бота

## ❌ Проблема
Бот не может запуститься из-за неправильной конфигурации. В файле `.env` установлены placeholder значения вместо реальных токенов.

## ✅ Решение

### 1. **Получите токен Telegram бота**

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен (формат: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. **Получите токен Marzban администратора**

1. Откройте ваш Marzban в браузере
2. Перейдите в Swagger UI: `https://your-marzban-domain.com/docs`
3. Нажмите кнопку **"Authorize"**
4. Введите:
   - **Username:** ваш админ логин
   - **Password:** ваш админ пароль
5. Скопируйте полученный токен (формат: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

### 3. **Обновите файл .env**

Замените содержимое файла `.env` на:

```bash
# Telegram Bot Token (получить у @BotFather)
USERBOT_TOKEN=ВАШ_ТОКЕН_БОТА_ЗДЕСЬ

# Marzban API настройки
MARZBAN_API_URL=https://alb-vpnprimex.duckdns.org/api
MARZBAN_ADMIN_TOKEN=ВАШ_ТОКЕН_MARZBAN_ЗДЕСЬ

# База данных
DATA_FILE=data.json

# Логирование
LOG_LEVEL=INFO
LOG_FILE=bot.log

# Безопасность
SECRET_KEY=your_secret_key_here
RATE_LIMIT_RPM=60
RATE_LIMIT_RPH=1000

# Мониторинг (опционально)
SENTRY_DSN=
PROMETHEUS_PORT=8000

# Redis (опционально)
REDIS_URL=redis://localhost:6379

# Платежи
DAILY_COST=4.0
MIN_BALANCE_WARNING=8.0

# Уведомления (опционально)
ADMIN_TELEGRAM_ID=
NOTIFICATION_ENABLED=true
```

### 4. **Проверьте конфигурацию**

```bash
python3 check_and_fix_config.py
```

### 5. **Запустите бота**

```bash
python3 main_improved.py
```

## 🔧 Альтернативный способ

Если у вас уже есть рабочие токены, вы можете обновить их напрямую:

```bash
# Обновите токен бота
sed -i 's/USERBOT_TOKEN=.*/USERBOT_TOKEN=ВАШ_ТОКЕН_БОТА/' .env

# Обновите токен Marzban
sed -i 's/MARZBAN_ADMIN_TOKEN=.*/MARZBAN_ADMIN_TOKEN=ВАШ_ТОКЕН_MARZBAN/' .env
```

## 🚨 Важные замечания

1. **Никогда не делитесь токенами** - они дают полный доступ к вашему боту и Marzban
2. **Проверьте URL Marzban** - убедитесь что `https://alb-vpnprimex.duckdns.org/api` доступен
3. **Создайте резервную копию** файла `.env` после настройки

## 🆘 Если проблемы остаются

1. Проверьте, что все токены скопированы полностью
2. Убедитесь, что нет лишних пробелов в `.env` файле
3. Проверьте доступность Marzban API
4. Запустите `python3 check_and_fix_config.py` для диагностики

## 📞 Поддержка

Если у вас возникли проблемы, проверьте:
- Логи бота в файле `bot.log`
- Доступность Marzban API
- Правильность токенов