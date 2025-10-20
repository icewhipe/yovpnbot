# Быстрый старт YOVPN Telegram Bot

## 🚀 Варианты запуска

### 1. Автономный режим (для тестирования)
**Используйте, если Marzban API недоступен или не настроен**

```bash
# Запуск автономной версии
python3 main_standalone.py
```

**Особенности:**
- ✅ Работает без Marzban API
- ✅ Все функции бота доступны
- ✅ Реферальная система работает
- ✅ QR-коды генерируются
- ⚠️ Подписки показываются как заглушки

### 2. Полный режим (с Marzban API)
**Используйте для продакшена**

```bash
# Сначала настройте .env файл
nano .env

# Затем запустите полную версию
python3 main_improved.py
```

## ⚙️ Настройка конфигурации

### Для автономного режима:
```bash
# Минимальная конфигурация
echo "USERBOT_TOKEN=your_telegram_bot_token" > .env
echo "MARZBAN_API_URL=https://test.com/api" >> .env
echo "MARZBAN_ADMIN_TOKEN=test_token" >> .env
echo "DB_PASSWORD=test_password" >> .env
```

### Для полного режима:
```bash
# Реальная конфигурация
nano .env
```

**Содержимое .env:**
```env
# Telegram Bot Configuration
USERBOT_TOKEN=your_actual_telegram_bot_token_here

# Marzban API Configuration
MARZBAN_API_URL=https://your-marzban-domain.com/api
MARZBAN_ADMIN_TOKEN=your_actual_marzban_admin_token_here

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=marzban
DB_USER=marzban
DB_PASSWORD=your_secure_database_password_here

# Data file path
DATA_FILE=data.json
```

## 🔧 Диагностика проблем

### Проблема: "Ошибка авторизации в Marzban API"
**Решение:**
1. Используйте автономный режим: `python3 main_standalone.py`
2. Или настройте реальные токены в `.env`

### Проблема: "No such file or directory: 'data.json'"
**Решение:**
```bash
# Создайте файл данных
touch data.json
echo '{}' > data.json
```

### Проблема: "ModuleNotFoundError"
**Решение:**
```bash
# Установите зависимости
pip3 install -r requirements.txt
```

## 📋 Чек-лист запуска

### Автономный режим:
- [ ] Установлены зависимости: `pip3 install -r requirements.txt`
- [ ] Настроен .env с токеном бота
- [ ] Запущен: `python3 main_standalone.py`
- [ ] Бот отвечает на команды

### Полный режим:
- [ ] Установлены зависимости: `pip3 install -r requirements.txt`
- [ ] Настроен .env с реальными токенами
- [ ] Marzban API доступен
- [ ] Запущен: `python3 main_improved.py`
- [ ] Бот отвечает на команды

## 🎯 Рекомендации

### Для разработки и тестирования:
- Используйте `main_standalone.py`
- Все функции работают
- Не требует настройки Marzban

### Для продакшена:
- Используйте `main_improved.py`
- Настройте реальные токены
- Настройте мониторинг

## 📞 Поддержка

### Если что-то не работает:
1. Проверьте логи
2. Запустите тест: `python3 test_marzban.py`
3. Проверьте конфигурацию: `cat .env`
4. Обратитесь к документации

### Полезные команды:
```bash
# Проверка импорта
python3 -c "import main_standalone; print('OK')"

# Запуск тестов
python3 -m pytest tests/ -v

# Проверка конфигурации
python3 test_marzban.py
```

## ✅ Готово!

Теперь у вас есть:
- ✅ Автономная версия для тестирования
- ✅ Полная версия для продакшена
- ✅ Инструкции по настройке
- ✅ Диагностика проблем
- ✅ Тесты и документация

**Выберите подходящий режим и запускайте бота!** 🚀