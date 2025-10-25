# 🚨 ВАЖНО: Сначала настройте конфигурацию!

## ⚡ Быстрый старт (3 команды)

```bash
# 1. Проверьте, что нужно настроить
python3 setup_check.py

# 2. Настройте токены в .env
nano .env

# 3. Запустите бота
python3 bot/main.py
```

---

## 📖 Где взять токены?

### 🤖 Токен Telegram бота
1. Telegram → @BotFather
2. Отправьте `/newbot`
3. Скопируйте токен

### 🔑 Токен Marzban
1. Откройте http://localhost:8000
2. Settings → API → Create Token
3. Скопируйте токен

---

## 📚 Подробная документация

- ⚡ **5 минут**: [`QUICK_SETUP.md`](QUICK_SETUP.md)
- 🔐 **Детали**: [`SETUP_TOKENS.md`](SETUP_TOKENS.md)
- 🏠 **Полная**: [`LOCAL_SETUP.md`](LOCAL_SETUP.md)

---

## 🔍 Проверка

```bash
python3 setup_check.py
```

**Должно быть**: ✅ Все проверки пройдены (5/5)

---

## 🆘 Проблемы?

```bash
cat SETUP_SUMMARY.txt
```

**Помощь**: [@YoVPNSupport](https://t.me/YoVPNSupport)
