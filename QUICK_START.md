# 🚀 Быстрый старт YoVPN

> **Версия:** 2.0  
> **Обновлено:** 22.10.2025

---

## 📋 Что это?

**YoVPN** — современный Telegram VPN-бот с WebApp интерфейсом, построенный на:

- 🤖 **aiogram 3** — Telegram Bot Framework
- 🌐 **Next.js 15** — WebApp (Telegram Mini App)
- ⚡ **FastAPI** — Backend API
- 🐘 **PostgreSQL** — База данных
- 🔐 **Marzban** — VPN Management Panel

---

## ⚡ Быстрый запуск (3 минуты)

### Вариант 1: Автоматический запуск

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/yourusername/yovpn.git
cd yovpn

# 2. Запустите установку
chmod +x install.sh
./install.sh

# 3. Настройте переменные окружения
cp .env.example .env
nano .env  # или vim, code, etc.

# 4. Запустите все сервисы
./start-webapp.sh
```

**Готово!** 🎉

- 🤖 Бот: работает
- 🌐 WebApp: http://localhost:3000
- ⚡ API: http://localhost:8000/docs

### Вариант 2: Ручной запуск

<details>
<summary>Развернуть пошаговую инструкцию</summary>

#### Terminal 1: Бот

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск бота
python -m bot.main
```

#### Terminal 2: API

```bash
cd api

# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установка
pip install -r requirements.txt

# Запуск
uvicorn app.main:app --reload
```

#### Terminal 3: WebApp

```bash
cd webapp

# Установка
npm install

# Запуск
npm run dev
```

</details>

---

## 🔧 Настройка `.env`

Создайте файл `.env` в корне проекта:

```env
# ═══════════════════════════════════════════
# 🤖 TELEGRAM BOT
# ═══════════════════════════════════════════
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHI...
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef...

# ═══════════════════════════════════════════
# 🐘 DATABASE
# ═══════════════════════════════════════════
DATABASE_URL=postgresql://user:password@localhost:5432/yovpn

# ═══════════════════════════════════════════
# 🔐 MARZBAN (VPN Panel)
# ═══════════════════════════════════════════
MARZBAN_URL=https://your-marzban.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=your-password

# ═══════════════════════════════════════════
# 🌐 SERVICES URLs
# ═══════════════════════════════════════════
API_URL=http://localhost:8000
WEBAPP_URL=http://localhost:3000

# ═══════════════════════════════════════════
# ⚙️ SETTINGS
# ═══════════════════════════════════════════
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Где взять токены?

#### 1. TELEGRAM_BOT_TOKEN

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

#### 2. TELEGRAM_API_ID и API_HASH

1. Откройте [my.telegram.org/apps](https://my.telegram.org/apps)
2. Войдите с вашим номером
3. Создайте приложение
4. Скопируйте API ID и API Hash

#### 3. DATABASE_URL

**Локально (Docker):**

```bash
docker run -d \
  --name yovpn-postgres \
  -e POSTGRES_USER=yovpn \
  -e POSTGRES_PASSWORD=your-password \
  -e POSTGRES_DB=yovpn \
  -p 5432:5432 \
  postgres:15-alpine
```

**DATABASE_URL:**
```
postgresql://yovpn:your-password@localhost:5432/yovpn
```

**Production (Railway):**

Railway автоматически создаст PostgreSQL и `DATABASE_URL`.

---

## 📁 Структура проекта

```
yovpn/
├── bot/                    # 🤖 Telegram Bot (aiogram)
│   ├── handlers/           # Обработчики команд и callback
│   ├── keyboards/          # Клавиатуры (InlineKeyboard)
│   ├── services/           # Бизнес-логика
│   ├── middleware/         # Middleware (logging, rate limit)
│   └── main.py             # Точка входа
│
├── webapp/                 # 🌐 Next.js WebApp
│   ├── src/
│   │   ├── app/            # Next.js 15 App Router
│   │   ├── components/     # React компоненты
│   │   ├── hooks/          # Custom hooks (useTelegram)
│   │   ├── lib/            # API клиент, utils
│   │   └── types/          # TypeScript типы
│   ├── package.json
│   └── Dockerfile
│
├── api/                    # ⚡ FastAPI Backend
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── models/         # Pydantic модели
│   │   ├── services/       # Сервисы (Marzban, User)
│   │   └── main.py         # FastAPI приложение
│   ├── requirements.txt
│   └── Dockerfile
│
├── .env                    # 🔐 Переменные окружения
├── docker-compose.yml      # 🐳 Docker Compose
├── requirements.txt        # 📦 Python зависимости (бот)
└── README.md               # 📖 Документация
```

---

## 🧪 Тестирование

### Локальное тестирование

```bash
# 1. Запустите все сервисы
./start-webapp.sh

# 2. Откройте Telegram
# 3. Найдите вашего бота
# 4. Отправьте /start
```

**Ожидаемое поведение:**

1. ✅ Бот отвечает приветственным сообщением
2. ✅ Показывается главное меню с кнопками
3. ✅ Кнопка "Подписка" работает
4. ✅ WebApp открывается (если настроен)

### Dev Mode для WebApp

Тестирование WebApp без Telegram:

```bash
cd webapp
cp .env.example .env.local

# Включите Dev Mode
echo "NEXT_PUBLIC_DEV_MODE=true" >> .env.local

npm run dev
```

Откройте http://localhost:3000 и нажмите 🛠️ в углу.

---

## 🚀 Деплой на Railway

### Быстрый деплой (5 минут)

```bash
# 1. Создайте проект на Railway
railway login
railway init

# 2. Добавьте PostgreSQL
railway add --service postgres

# 3. Deploy!
railway up
```

### Подробная инструкция

См. **[RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md](./RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md)**

---

## 📖 Документация

### Основные документы

- **[README.md](./README.md)** — Полная документация проекта
- **[QUICK_START.md](./QUICK_START_UPDATED.md)** — Быстрый старт (этот файл)
- **[RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md](./RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md)** — Полное руководство по деплою
- **[WEBAPP_GUIDE.md](./WEBAPP_GUIDE.md)** — Документация WebApp
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** — Архитектура проекта

### Дополнительные

- **[CHANGELOG.md](./CHANGELOG.md)** — История изменений
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** — Как контрибутить
- **[LICENSE](./LICENSE)** — Лицензия

---

## ❓ Частые вопросы (FAQ)

### 1. Ошибка `sh: next: not found` при деплое

**Решение:**

1. Проверьте, что `next` в `dependencies`, не в `devDependencies`
2. В Dockerfile используйте `CMD ["node", "server.js"]`
3. В `next.config.js` установите `output: 'standalone'`

См. подробности: [RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md](./RAILWAY_DEPLOYMENT_COMPLETE_GUIDE.md)

### 2. Бот не отвечает

**Проверьте:**

1. `TELEGRAM_BOT_TOKEN` правильный?
2. Бот запущен? (`python -m bot.main`)
3. Логи: есть ошибки?

```bash
# Проверка
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### 3. WebApp не открывается

**Решение:**

1. Telegram требует **HTTPS** (не работает с `http://`)
2. Используйте ngrok для локального тестирования:

```bash
ngrok http 3000
```

3. Обновите `WEBAPP_URL` в `.env`

### 4. DATABASE_URL ошибка

**Формат:**

```
postgresql://user:password@host:port/database
```

**Railway автоматически создает** `${{Postgres.DATABASE_URL}}`

### 5. Как добавить нового пользователя в админку?

```python
# В bot/handlers/admin_handler.py
ADMIN_IDS = [123456789, 987654321]  # Ваши Telegram ID
```

Узнать свой ID: [@userinfobot](https://t.me/userinfobot)

---

## 🆘 Поддержка

Нужна помощь?

1. 📖 Читайте [полную документацию](./README.md)
2. 🐛 Откройте [GitHub Issue](https://github.com/yourusername/yovpn/issues)
3. 💬 Telegram: [@yovpn_support](https://t.me/yovpn_support)
4. ✉️ Email: support@yovpn.com

---

## ✅ Чек-лист "Всё работает"

После установки проверьте:

- [ ] Бот отвечает на `/start`
- [ ] Главное меню показывается
- [ ] API доступен на `/docs`
- [ ] WebApp открывается (если настроен)
- [ ] PostgreSQL подключен
- [ ] Marzban интеграция работает (если настроена)

**Всё работает?** 🎉 **Поздравляем!**

---

## 📊 Что дальше?

### Локальная разработка

1. Изучите структуру проекта
2. Добавьте свои функции
3. Тестируйте локально

### Production деплой

1. Деплой на Railway (см. гайд)
2. Настройте домен
3. Включите HTTPS
4. Настройте мониторинг

### Кастомизация

1. Измените тексты бота (`bot/utils/texts.py`)
2. Добавьте новые кнопки (`bot/keyboards/menu_kb.py`)
3. Настройте дизайн WebApp (`webapp/src/styles/globals.css`)

---

## 🎯 Полезные команды

```bash
# Запуск всех сервисов
./start-webapp.sh

# Остановка
./stop-webapp.sh

# Только бот
python -m bot.main

# Только API
cd api && uvicorn app.main:app --reload

# Только WebApp
cd webapp && npm run dev

# Docker Compose (всё сразу)
docker-compose up -d

# Логи
docker-compose logs -f

# Остановка Docker
docker-compose down
```

---

**Удачи в разработке! 🚀**

*Если возникли вопросы — читайте [полную документацию](./README.md) или обращайтесь в [поддержку](#-поддержка).*
