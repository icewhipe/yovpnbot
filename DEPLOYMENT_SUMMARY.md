# 📦 YoVPN - Полная Инструкция по Деплою

## 🎯 Что было создано

Я подготовил полный набор документации и конфигураций для деплоя вашего проекта YoVPN на Railway (и опционально Vercel).

---

## 📚 Созданные файлы

### 1. **RAILWAY_DEPLOYMENT_GUIDE.md** ⭐ (ГЛАВНЫЙ ДОКУМЕНТ)
   - **Описание**: Полное пошаговое руководство по деплою
   - **Содержание**:
     - Вариант 1: Все на Railway (рекомендуется)
     - Вариант 2: WebApp на Vercel + остальное на Railway
     - Подготовка переменных окружения
     - Настройка всех 4 сервисов
     - Troubleshooting
     - Мониторинг
   - **Когда использовать**: Главная инструкция, начните отсюда

### 2. **DEPLOYMENT_CHECKLIST.md** ✅
   - **Описание**: Краткий чеклист с чекбоксами
   - **Содержание**:
     - Пошаговый список задач
     - Места для записи токенов и URL
     - Быстрая настройка переменных
     - Частые проблемы
   - **Когда использовать**: Во время деплоя, чтобы ничего не забыть

### 3. **ARCHITECTURE.md** 🏗️
   - **Описание**: Визуальная схема архитектуры
   - **Содержание**:
     - ASCII диаграммы архитектуры
     - Поток данных между сервисами
     - Детальное описание каждого сервиса
     - Безопасность и масштабирование
   - **Когда использовать**: Для понимания общей картины

### 4. **railway-configs/** 📂
   Директория с конфигурациями для Railway:
   
   - **bot.railway.json** - конфиг для Telegram бота
   - **api.railway.json** - конфиг для API backend
   - **webapp.railway.json** - конфиг для WebApp frontend
   - **README.md** - описание конфигураций

### 5. **railway.json** и **railway.toml**
   - Конфигурационные файлы для Railway в корне проекта

---

## 🚀 Быстрый старт

### Что нужно сделать (5 шагов):

#### 1️⃣ Подготовка (5 минут)
```bash
# Получите токен бота
@BotFather → /newbot → сохраните токен

# Сгенерируйте секретный ключ
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Подготовьте данные Marzban
- URL: https://your-marzban.com
- Username: admin
- Password: ваш_пароль
```

#### 2️⃣ Railway Setup (5 минут)
1. Откройте [railway.app](https://railway.app)
2. Deploy from GitHub repo
3. Выберите ваш репозиторий

#### 3️⃣ Создание сервисов (10 минут)
```
+ New → Database → Redis
+ New → Empty Service → "telegram-bot"
+ New → Empty Service → "api"
+ New → Empty Service → "webapp"
```

#### 4️⃣ Настройка переменных (5 минут)
Для каждого сервиса скопируйте переменные из **DEPLOYMENT_CHECKLIST.md**

#### 5️⃣ Финализация (3 минуты)
- Сгенерируйте публичные URL для API и WebApp
- Обновите CORS_ORIGINS в API
- Настройте Menu Button в BotFather

**Готово! ✨**

---

## 📖 Рекомендуемый порядок чтения

### Для новичков:
1. **DEPLOYMENT_CHECKLIST.md** - начните здесь, следуйте пошагово
2. **RAILWAY_DEPLOYMENT_GUIDE.md** - детальная инструкция с примерами
3. **ARCHITECTURE.md** - чтобы понять, как всё работает

### Для опытных:
1. **ARCHITECTURE.md** - общая картина
2. **railway-configs/README.md** - технические детали
3. **DEPLOYMENT_CHECKLIST.md** - быстрый чеклист

### При проблемах:
1. **DEPLOYMENT_CHECKLIST.md** → Раздел "Частые проблемы"
2. **RAILWAY_DEPLOYMENT_GUIDE.md** → Раздел "Troubleshooting"
3. Проверьте логи в Railway Dashboard

---

## 🎯 Два варианта деплоя

### Вариант 1: Всё на Railway (Рекомендуется)
```
✅ Проще настроить
✅ Всё в одном месте
✅ Единый dashboard
✅ Внутренняя сеть между сервисами
✅ $0-5/месяц

Сервисы:
- Redis (база данных)
- telegram-bot (Python)
- api (FastAPI)
- webapp (Next.js)
```

### Вариант 2: WebApp на Vercel + Остальное на Railway
```
✅ Лучшая производительность для WebApp
✅ Больше бесплатных ресурсов для Next.js
✅ Vercel CI/CD для frontend
✅ $0/месяц (в пределах бесплатных лимитов)

Сервисы:
Railway:
- Redis
- telegram-bot (Python)
- api (FastAPI)

Vercel:
- webapp (Next.js)
```

---

## 🔑 Критические переменные

Эти переменные **ОБЯЗАТЕЛЬНЫ** для всех сервисов:

```bash
TELEGRAM_BOT_TOKEN=        # От @BotFather
SECRET_KEY=                # Сгенерированный ключ
MARZBAN_API_URL=          # URL вашего Marzban
MARZBAN_USERNAME=         # Админ Marzban
MARZBAN_PASSWORD=         # Пароль Marzban
```

---

## 📊 Структура проекта

```
yovpn/
├── bot/                           # Telegram Bot
│   ├── handlers/                  # Обработчики команд
│   ├── services/                  # Бизнес-логика
│   └── main.py                    # Точка входа
│
├── api/                           # Backend API
│   ├── app/                       # FastAPI приложение
│   ├── Dockerfile                 # Docker образ
│   └── requirements.txt           # Python зависимости
│
├── webapp/                        # Frontend WebApp
│   ├── src/                       # Next.js приложение
│   ├── Dockerfile                 # Docker образ
│   └── package.json               # Node зависимости
│
├── railway-configs/               # ⭐ Railway конфигурации
│   ├── bot.railway.json
│   ├── api.railway.json
│   ├── webapp.railway.json
│   └── README.md
│
├── RAILWAY_DEPLOYMENT_GUIDE.md    # ⭐ Главная инструкция
├── DEPLOYMENT_CHECKLIST.md        # ⭐ Чеклист
├── ARCHITECTURE.md                # ⭐ Архитектура
├── railway.json                   # Railway конфиг
└── railway.toml                   # Railway конфиг
```

---

## ⏱️ Сколько времени займёт?

```
Подготовка:                  5 минут
Railway Setup:               5 минут
Создание сервисов:          10 минут
Настройка переменных:        5 минут
Генерация URL:               2 минуты
Финальная настройка:         3 минуты
─────────────────────────────────────
ИТОГО:                      30 минут
```

---

## 💰 Стоимость

### Railway (Вариант 1)

```
Free Tier:
├── $5 кредитов в месяц (бесплатно)
├── 4 сервиса × ~$1.25 = ~$5/месяц
└── Итого: $0/месяц (в пределах free tier)

Если превысите лимит:
└── ~$5-10/месяц для небольшого проекта
```

### Vercel + Railway (Вариант 2)

```
Vercel (WebApp):
└── $0/месяц (Hobby tier)

Railway (Bot + API + Redis):
├── 3 сервиса × ~$1.67 = ~$5/месяц
└── Итого: $0/месяц (в пределах free tier)
```

**Рекомендация**: Начните с бесплатных тиров, upgrade по мере роста.

---

## ✅ Чеклист готовности к деплою

Перед началом убедитесь, что у вас есть:

- [ ] Аккаунт на [railway.app](https://railway.app)
- [ ] Токен бота от @BotFather
- [ ] Доступ к Marzban серверу (URL, username, password)
- [ ] Репозиторий на GitHub (с вашим кодом)
- [ ] 30 свободных минут

---

## 🐛 Что делать если что-то не работает?

### 1. Проверьте логи
```
Railway Dashboard → Выберите сервис → Logs
```

### 2. Проверьте переменные
```
Railway Dashboard → Выберите сервис → Variables
```

### 3. Проверьте статус
```
Railway Dashboard → Deployments
Статус должен быть: "Active" (зелёный)
```

### 4. Распространённые ошибки

| Проблема | Решение |
|----------|---------|
| Бот не отвечает | Проверьте TELEGRAM_BOT_TOKEN |
| API не отвечает | Проверьте CORS_ORIGINS |
| WebApp не загружается | Проверьте NEXT_PUBLIC_API_BASE_URL |
| Build failed | Проверьте Root Directory |
| Out of memory | Увеличьте RAM или оптимизируйте код |

### 5. Где искать помощь

1. **RAILWAY_DEPLOYMENT_GUIDE.md** → Раздел "Troubleshooting"
2. **DEPLOYMENT_CHECKLIST.md** → Раздел "Частые проблемы"
3. Railway Dashboard → Logs (детальные ошибки)
4. GitHub Issues (если баг в коде)

---

## 🎓 Дополнительные ресурсы

### Официальная документация:
- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Aiogram Docs](https://docs.aiogram.dev/)

### Полезные ссылки:
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram WebApp API](https://core.telegram.org/bots/webapps)
- [Marzban Documentation](https://github.com/Gozargah/Marzban)

---

## 📞 Следующие шаги

После успешного деплоя:

1. ✅ **Протестируйте бота**
   - Отправьте `/start`
   - Проверьте все команды
   - Протестируйте платежи

2. ✅ **Протестируйте WebApp**
   - Откройте URL в браузере
   - Проверьте мобильную версию
   - Протестируйте активацию

3. ✅ **Настройте мониторинг**
   - UptimeRobot для uptime
   - Sentry для ошибок
   - Analytics для метрик

4. ✅ **Настройте домен** (опционально)
   - Купите домен
   - Настройте DNS
   - Добавьте в Railway/Vercel

5. ✅ **Оптимизируйте**
   - Настройте кэширование
   - Оптимизируйте изображения
   - Настройте CDN

---

## 🎉 Готово!

Теперь у вас есть всё необходимое для деплоя YoVPN:

1. ✅ Полная документация
2. ✅ Конфигурационные файлы
3. ✅ Чеклисты и гайды
4. ✅ Troubleshooting советы
5. ✅ Архитектурная схема

**Начните с DEPLOYMENT_CHECKLIST.md и следуйте шаг за шагом!**

---

## 📝 Обратная связь

Если у вас есть вопросы или предложения по улучшению документации:
1. Создайте Issue на GitHub
2. Предложите Pull Request
3. Напишите в Telegram

---

**Успешного деплоя! 🚀**

*Документация обновлена: 21.10.2025*
