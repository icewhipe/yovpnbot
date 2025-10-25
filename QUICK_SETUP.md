# ⚡ YoVPN Bot - Быстрая настройка

## 🚨 Текущая проблема

```
❌ Отсутствуют обязательные настройки: BOT_TOKEN, MARZBAN_API_URL, MARZBAN_ADMIN_TOKEN
💥 Фатальная ошибка: Token is invalid!
```

## ✅ Быстрое решение (5 минут)

### 1️⃣ Получите токен Telegram бота

```bash
# Откройте Telegram → @BotFather
# Отправьте: /newbot
# Скопируйте токен вида: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 2️⃣ Получите токен Marzban

```bash
# Откройте панель Marzban: http://localhost:8000
# Settings → API → Create Token
# Скопируйте токен (начинается с eyJ...)
```

### 3️⃣ Откройте файл .env

```bash
nano .env
# или
vim .env
```

### 4️⃣ Замените эти строки:

```bash
# Было:
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
MARZBAN_ADMIN_TOKEN=YOUR_MARZBAN_TOKEN_HERE

# Стало:
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
MARZBAN_ADMIN_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 5️⃣ Проверьте настройки

```bash
python3 setup_check.py
```

Должно быть:
```
✅ Все проверки пройдены (5/5)
```

### 6️⃣ Запустите бота

```bash
python3 bot/main.py
```

---

## 📖 Подробная инструкция

Если нужны детали: [`SETUP_TOKENS.md`](SETUP_TOKENS.md)

---

## 🔧 Команды для проверки

```bash
# Проверка конфигурации
python3 setup_check.py

# Проверка переменных окружения
python3 check_env.py

# Просмотр .env
cat .env

# Запуск бота
python3 bot/main.py
```

---

## 🆘 Не работает?

### Marzban не установлен?

```bash
sudo bash -c "$(curl -sL https://github.com/Gozargah/Marzban-scripts/raw/master/marzban.sh)" @ install
```

### Токен бота не работает?

```bash
# Получите новый токен у @BotFather:
# /mybots → выберите бота → API Token
```

### Ошибка подключения к Marzban?

```bash
# Проверьте доступность:
curl http://localhost:8000/api/core/

# Проверьте, что Marzban запущен:
docker ps | grep marzban
```

---

## ✅ Готово!

После настройки запустите:

```bash
python3 bot/main.py
```

Вы должны увидеть:

```
✅ Блокировка получена (PID: 12345)
🚀 Запуск YoVPN Bot...
YoVPN Bot инициализирован
```

**Бот готов к работе!** 🎉

---

**Создано**: 2025-10-24  
**Время настройки**: ~5 минут  
**Помощь**: [@YoVPNSupport](https://t.me/YoVPNSupport)
