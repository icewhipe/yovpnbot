# 🔧 YoVPN Bot - Руководство по настройке

## 📋 Краткое содержание

Это руководство поможет вам настроить и запустить YoVPN Bot локально или на сервере.

---

## 📚 Документация по настройке

| Файл | Описание | Когда использовать |
|------|----------|-------------------|
| **SETUP_SUMMARY.txt** | Краткая справка (ASCII) | Быстрая шпаргалка |
| **QUICK_SETUP.md** | Быстрая настройка (5 мин) | Первый запуск |
| **SETUP_TOKENS.md** | Подробная настройка токенов | Нужны детали |
| **LOCAL_SETUP.md** | Полная локальная установка | Первый раз запускаете |
| **setup_check.py** | Скрипт проверки | Диагностика |

---

## 🚀 Быстрый старт

### 1. Первый запуск (настройка токенов)

```bash
# Посмотрите краткую справку
cat SETUP_SUMMARY.txt

# Или прочитайте быструю настройку
cat QUICK_SETUP.md
```

### 2. Проверка настроек

```bash
python3 setup_check.py
```

### 3. Запуск бота

```bash
python3 bot/main.py
```

---

## 📖 Подробные инструкции

### Для локальной разработки
→ [`LOCAL_SETUP.md`](LOCAL_SETUP.md)

### Для деплоя на Railway
→ [`START_HERE.md`](START_HERE.md)

### Для настройки токенов
→ [`SETUP_TOKENS.md`](SETUP_TOKENS.md)

---

## 🔑 Что нужно настроить

### Обязательные параметры:

1. **TELEGRAM_BOT_TOKEN** (или BOT_TOKEN)
   - Получить: @BotFather → `/newbot`
   - Формат: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

2. **MARZBAN_ADMIN_TOKEN**
   - Получить: Marzban Panel → Settings → API
   - Формат: `eyJhbGciOiJIUzI1NiIs...`

3. **MARZBAN_API_URL**
   - Пример: `http://localhost:8000`
   - Или: `https://your-domain.com`

### Опциональные параметры:

- `ADMIN_TG_ID` - ваш Telegram ID (узнать у @userinfobot)
- `DATABASE_URL` - подключение к базе данных
- `REDIS_URL` - подключение к Redis
- `DAILY_PRICE` - цена за день (по умолчанию 4.0)
- `WELCOME_BONUS` - приветственный бонус (по умолчанию 12.0)

---

## 🔍 Диагностика

### Проверка конфигурации
```bash
python3 setup_check.py
```

### Проверка переменных окружения
```bash
python3 check_env.py
```

### Проверка settings.py
```bash
python3 config/settings.py
```

### Просмотр .env
```bash
cat .env
```

### Просмотр логов
```bash
tail -f /tmp/yovpn.log
```

---

## ❌ Решение проблем

### Ошибка: "Token is invalid!"

**Решение:**
```bash
# 1. Проверьте токен в .env
cat .env | grep TELEGRAM_BOT_TOKEN

# 2. Получите новый токен
# Telegram → @BotFather → /token

# 3. Замените в .env
nano .env
```

### Ошибка: "MARZBAN_API_URL is required"

**Решение:**
```bash
# Убедитесь, что в .env есть:
MARZBAN_API_URL=http://localhost:8000
```

### Ошибка: "Connection refused" к Marzban

**Решение:**
```bash
# Проверьте, что Marzban запущен
docker ps | grep marzban

# Проверьте доступность
curl http://localhost:8000/api/core/

# Если не установлен, установите:
sudo bash -c "$(curl -sL https://github.com/Gozargah/Marzban-scripts/raw/master/marzban.sh)" @ install
```

### Ошибка: "No module named 'aiogram'"

**Решение:**
```bash
pip install -r requirements.txt
```

---

## 📁 Структура файлов конфигурации

```
/workspace/
├── .env                      # Основной конфигурационный файл ⚠️ НАСТРОЙТЕ ЗДЕСЬ
├── .env.example              # Пример конфигурации
├── .env.sample               # Альтернативный пример
│
├── setup_check.py            # Скрипт проверки настроек ✅ ЗАПУСТИТЕ ПЕРВЫМ
├── check_env.py              # Проверка переменных окружения
│
├── SETUP_SUMMARY.txt         # Краткая справка (ASCII)
├── QUICK_SETUP.md            # Быстрая настройка (5 мин)
├── SETUP_TOKENS.md           # Подробная настройка токенов
├── LOCAL_SETUP.md            # Локальная установка
├── CONFIGURATION_GUIDE.md    # Это руководство
│
├── config/
│   └── settings.py           # Настройки (config/settings.py)
├── src/config/
│   ├── config.py             # Конфигурация бота
│   └── settings.py           # Альтернативные настройки
└── config.py                 # Базовая конфигурация
```

---

## ✅ Чеклист готовности

Перед запуском проверьте:

- [ ] Python 3.8+ установлен
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] Файл `.env` создан и настроен
- [ ] Токен бота получен и добавлен в `.env`
- [ ] Токен Marzban получен и добавлен в `.env`
- [ ] URL Marzban указан в `.env`
- [ ] Проверка пройдена (`python3 setup_check.py` → ✅ 5/5)
- [ ] Бот запускается без ошибок (`python3 bot/main.py`)

---

## 🎯 Следующие шаги

После успешной настройки:

1. ✅ Протестируйте бота в Telegram
2. ✅ Настройте админ-панель: `python3 admin/main.py`
3. ✅ Прочитайте [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md)
4. ✅ Настройте платежную систему
5. ✅ Настройте реферальную программу

---

## 🔗 Полезные ссылки

- 📖 [Основная документация](README.md)
- 🏗️ [Архитектура проекта](ARCHITECTURE.md)
- 🚀 [Деплой на Railway](START_HERE.md)
- 📚 [Что реализовано](ЧТО_РЕАЛИЗОВАНО.md)
- 🐛 [Исправления багов](BUGFIX_SUMMARY_RU.md)

---

## 💬 Поддержка

**Проблемы с настройкой?**

1. 🔍 Запустите: `python3 setup_check.py`
2. 📖 Прочитайте: `cat SETUP_TOKENS.md`
3. 🔧 Проверьте: `cat .env`
4. 💬 Напишите: [@YoVPNSupport](https://t.me/YoVPNSupport)
5. 🐛 Создайте issue на GitHub

---

## 📌 Важные замечания

⚠️ **Безопасность:**
- Никогда не публикуйте файл `.env` в Git
- Храните токены в безопасности
- Используйте сильные пароли для баз данных

⚠️ **Marzban:**
- Убедитесь, что Marzban запущен и доступен
- Проверьте версию Marzban (рекомендуется последняя)
- Создайте резервные копии данных

⚠️ **База данных:**
- Для продакшена используйте MySQL
- Для тестирования можно использовать SQLite
- Регулярно делайте бэкапы

---

**Создано**: 2025-10-24  
**Версия**: 1.0.0  
**Статус**: ✅ Готово к использованию

---

**Удачной настройки! 🚀**
