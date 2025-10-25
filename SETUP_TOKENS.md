# 🔐 Инструкция по настройке токенов YoVPN Bot

## ❌ Текущая проблема

Вы видите эти ошибки:
```
❌ Отсутствуют обязательные настройки: BOT_TOKEN, MARZBAN_API_URL, MARZBAN_ADMIN_TOKEN
⚠️ Внимание: Конфигурация неполная. Проверьте переменные окружения.
💥 Фатальная ошибка: Token is invalid!
```

## ✅ Решение (3 простых шага)

### Шаг 1: Получите токен Telegram бота

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте команду `/newbot`
3. Придумайте имя бота (например: `YoVPN Bot`)
4. Придумайте username бота (например: `yovpn_test_bot`)
5. **BotFather даст вам токен** вида: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

**Скопируйте этот токен!** ✅

---

### Шаг 2: Получите токен Marzban API

#### Вариант А: Если Marzban уже установлен

1. Откройте панель Marzban в браузере (например: `http://localhost:8000`)
2. Войдите под учетной записью администратора
3. Перейдите в **Settings** → **API**
4. Нажмите **Create Token** или скопируйте существующий
5. **Скопируйте токен** (длинная строка вида: `eyJhbGciOi...`)

#### Вариант Б: Если Marzban НЕ установлен

Сначала установите Marzban:

```bash
# Ubuntu/Debian
sudo bash -c "$(curl -sL https://github.com/Gozargah/Marzban-scripts/raw/master/marzban.sh)" @ install
```

После установки:
- URL: `http://localhost:8000`
- Логин: `admin`
- Пароль: будет показан при установке

Затем выполните **Вариант А**.

---

### Шаг 3: Настройте файл .env

Откройте файл `/workspace/.env` и замените значения:

```bash
# Замените YOUR_BOT_TOKEN_HERE на токен от @BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Замените YOUR_MARZBAN_TOKEN_HERE на токен из панели Marzban
MARZBAN_ADMIN_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Если Marzban на другом сервере, замените URL
MARZBAN_API_URL=http://localhost:8000
```

---

## 🚀 Запуск бота

После настройки токенов запустите бота:

```bash
cd /workspace
python3 bot/main.py
```

Если всё настроено правильно, вы увидите:

```
✅ Блокировка получена (PID: 12345)
🚀 Запуск YoVPN Bot...
YoVPN Bot инициализирован
```

---

## 🔍 Проверка конфигурации

Проверьте настройки командой:

```bash
python3 check_env.py
```

Или:

```bash
python3 config/settings.py
```

---

## 🆘 Частые проблемы

### Проблема: "Token is invalid!"

**Причина**: Токен бота неправильный или пустой.

**Решение**:
1. Убедитесь, что скопировали токен полностью
2. Проверьте, что в `.env` нет пробелов вокруг токена
3. Получите новый токен у @BotFather командой `/token`

---

### Проблема: "MARZBAN_API_URL is required"

**Причина**: Не указан URL Marzban или он неправильный.

**Решение**:
1. Проверьте, что Marzban запущен
2. Убедитесь, что URL правильный (например: `http://192.168.1.100:8000`)
3. Проверьте доступность: `curl http://localhost:8000/api/core/`

---

### Проблема: "MARZBAN_ADMIN_TOKEN is required"

**Причина**: Не указан токен Marzban.

**Решение**:
1. Войдите в панель Marzban
2. Создайте новый токен в Settings → API
3. Скопируйте токен целиком в `.env`

---

## 📚 Дополнительная информация

- 📖 [Документация Marzban](https://github.com/Gozargah/Marzban)
- 📖 [Документация Bot API](https://core.telegram.org/bots)
- 📖 [Руководство по установке](INSTALL_GUIDE.md)

---

## 💬 Нужна помощь?

Если проблема не решается:

1. Проверьте логи: `tail -f /tmp/yovpn.log`
2. Напишите в поддержку: @YoVPNSupport
3. Создайте issue на GitHub

---

**Создано**: 2025-10-24
**Автор**: YoVPN Team
