# 🏠 YoVPN Bot - Локальная установка

## ⚠️ Видите ошибку при запуске?

```
❌ Отсутствуют обязательные настройки: BOT_TOKEN, MARZBAN_API_URL, MARZBAN_ADMIN_TOKEN
💥 Фатальная ошибка: Token is invalid!
```

**Это нормально!** Просто нужно настроить токены. Следуйте инструкции ниже ⬇️

---

## ⚡ Быстрая настройка (5 минут)

### Шаг 1: Установите зависимости

```bash
pip install -r requirements.txt
```

### Шаг 2: Получите токены

#### 🤖 Токен Telegram бота

1. Откройте Telegram → @BotFather
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. **Скопируйте токен** (например: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 🔑 Токен Marzban

**Вариант А: Marzban уже установлен**
1. Откройте панель Marzban: `http://localhost:8000`
2. Settings → API → Create Token
3. **Скопируйте токен** (начинается с `eyJ...`)

**Вариант Б: Marzban не установлен**
```bash
# Установите Marzban
sudo bash -c "$(curl -sL https://github.com/Gozargah/Marzban-scripts/raw/master/marzban.sh)" @ install

# После установки:
# URL: http://localhost:8000
# Логин: admin
# Пароль: будет показан при установке
```

### Шаг 3: Настройте .env файл

```bash
# Откройте .env в редакторе
nano .env
# или
vim .env
```

**Замените эти строки:**

```bash
# ДО:
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
MARZBAN_ADMIN_TOKEN=YOUR_MARZBAN_TOKEN_HERE

# ПОСЛЕ:
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
MARZBAN_ADMIN_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Если Marzban на другом сервере:
```bash
MARZBAN_API_URL=http://192.168.1.100:8000
```

### Шаг 4: Проверьте настройки

```bash
python3 setup_check.py
```

**Ожидаемый результат:**
```
✅ Файл .env найден
✅ Токен бота найден: 1234567890...
✅ URL Marzban: http://localhost:8000
✅ Токен Marzban найден: eyJhbGci...
✅ База данных: localhost:3306/yovpn

✅ Все проверки пройдены (5/5)
ℹ️  Можно запускать бота:
   python3 bot/main.py
```

### Шаг 5: Запустите бота

```bash
python3 bot/main.py
```

**Успешный запуск выглядит так:**
```
✅ Блокировка получена (PID: 12345)
🚀 Запуск YoVPN Bot...
YoVPN Bot инициализирован
```

**Готово! Бот работает!** 🎉

---

## 🔧 Дополнительные компоненты

### Админ-панель

```bash
python3 admin/main.py
```

Откройте в браузере: http://localhost:8080

### WebApp (опционально)

```bash
cd webapp
npm install
npm run dev
```

Откройте в браузере: http://localhost:3000

### Все сервисы сразу

```bash
python3 run_all.py
```

---

## 📋 Полная конфигурация .env

```bash
# === TELEGRAM BOT ===
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
BOT_TOKEN=ваш_токен_от_BotFather
ADMIN_TG_ID=ваш_telegram_id

# === MARZBAN API ===
MARZBAN_API_URL=http://localhost:8000
MARZBAN_ADMIN_TOKEN=ваш_токен_из_marzban

# === DATABASE ===
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/yovpn
# или для SQLite (для тестирования):
# DATABASE_URL=sqlite:///data.json

# === REDIS (для кэша) ===
REDIS_URL=redis://localhost:6379/0

# === НАСТРОЙКИ ===
DEBUG=False
LOG_LEVEL=INFO
DAILY_PRICE=4.0
WELCOME_BONUS=12.0
```

---

## 🔍 Проверка и отладка

### Проверка конфигурации
```bash
python3 setup_check.py
```

### Проверка переменных окружения
```bash
python3 check_env.py
```

### Просмотр логов
```bash
tail -f /tmp/yovpn.log
```

### Проверка подключения к Marzban
```bash
curl http://localhost:8000/api/core/
```

---

## 🆘 Частые проблемы и решения

### ❌ "Token is invalid!"

**Причина**: Неправильный или пустой токен бота.

**Решение**:
1. Проверьте, что скопировали токен полностью
2. Убедитесь, что нет пробелов в начале/конце
3. Получите новый токен: @BotFather → `/token`

---

### ❌ "MARZBAN_API_URL is required"

**Причина**: Не указан URL Marzban.

**Решение**:
```bash
# В .env добавьте:
MARZBAN_API_URL=http://localhost:8000
```

---

### ❌ "Connection refused" при подключении к Marzban

**Причина**: Marzban не запущен или недоступен.

**Решение**:
```bash
# Проверьте, что Marzban запущен:
docker ps | grep marzban

# Проверьте доступность:
curl http://localhost:8000/api/core/

# Если нужно, запустите Marzban:
marzban start
```

---

### ❌ "No module named 'aiogram'"

**Причина**: Не установлены зависимости.

**Решение**:
```bash
pip install -r requirements.txt
```

---

### ❌ База данных не работает

**Для MySQL:**
```bash
# Убедитесь, что MySQL запущен:
sudo systemctl start mysql

# Создайте базу данных:
mysql -u root -p
CREATE DATABASE yovpn;
exit
```

**Для SQLite (тестирование):**
```bash
# В .env замените:
DATABASE_URL=sqlite:///data.json
```

---

## 📊 Узнать свой Telegram ID

```bash
# Напишите боту @userinfobot в Telegram
# Он ответит вашим ID
```

Или используйте:
```python
# В боте добавьте временно:
print(f"Your ID: {message.from_user.id}")
```

---

## 🎯 Следующие шаги

После успешного запуска:

1. ✅ Протестируйте бота в Telegram
2. ✅ Настройте админ-панель
3. ✅ Настройте платежную систему
4. ✅ Настройте реферальную систему
5. ✅ Прочитайте [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md)

---

## 📚 Дополнительная документация

- 📖 [README.md](README.md) - Основная документация
- 🔐 [SETUP_TOKENS.md](SETUP_TOKENS.md) - Подробная настройка токенов
- ⚡ [QUICK_SETUP.md](QUICK_SETUP.md) - Быстрая шпаргалка
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура проекта
- 🚀 [START_HERE.md](START_HERE.md) - Деплой на Railway

---

## 💬 Поддержка

Если проблема не решается:

1. 📖 Прочитайте [SETUP_TOKENS.md](SETUP_TOKENS.md)
2. 🔍 Запустите `python3 setup_check.py`
3. 📝 Проверьте логи: `tail -f /tmp/yovpn.log`
4. 💬 Создайте issue на GitHub
5. 📧 Напишите [@YoVPNSupport](https://t.me/YoVPNSupport)

---

## ✅ Чеклист готовности

- [ ] Python 3.8+ установлен
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] Файл .env создан и настроен
- [ ] Токен бота получен от @BotFather
- [ ] Токен Marzban получен из панели
- [ ] Проверка пройдена (`python3 setup_check.py`)
- [ ] Бот запущен без ошибок
- [ ] Бот отвечает в Telegram

**Если все галочки стоят - поздравляем! Бот работает! 🎉**

---

**Обновлено**: 2025-10-24  
**Время настройки**: ~5-10 минут  
**Помощь**: [@YoVPNSupport](https://t.me/YoVPNSupport)
