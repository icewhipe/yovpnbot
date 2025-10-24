# 💎 YoVPN Bot - Расширенная версия

## 🆕 Новые возможности

### 🤖 Текстовый режим

Полнофункциональный текстовый режим работы бота без WebApp:

- ✅ Анимированный `/start` с приветственным бонусом
- ✅ Проверка подписки на канал @yodevelop
- ✅ 3-шаговая активация VPN
- ✅ Реферальная система с 5 уровнями

### 👥 Реферальная программа

Многоуровневая реферальная система с автоматическим начислением бонусов:

```
Уровень 1: 10% от пополнений рефералов
Уровень 2: 5% от пополнений рефералов 2-го уровня
Уровень 3: 3% от пополнений рефералов 3-го уровня
Уровень 4: 2% от пополнений рефералов 4-го уровня
Уровень 5: 1% от пополнений рефералов 5-го уровня
```

**Бонус за приглашение:** 1 день VPN (4 рубля)

### ⚙️ Расширенная админ-панель

#### 📊 Статистика
- **Общая статистика** - пользователи, подписки, финансы
- **Статистика пользователей** - по периодам, топ рефереров
- **Финансовая статистика** - доход, транзакции, рефералы
- **Статистика Marzban** - подписки, трафик, статусы

#### 💰 Управление балансом
- **Пополнение баланса** - добавление средств пользователям
- **Списание баланса** - списание средств
- **Установка баланса** - установка конкретной суммы
- **Поиск пользователей** - для операций с балансом

#### 🔧 Настройки Marzban
- **Тест соединения** - проверка API
- **Синхронизация** - синхронизация подписок с Marzban
- **Список пользователей** - все пользователи в Marzban

#### 🛡️ Безопасность
- **Логи** - просмотр логов системы
- **Мониторинг** - мониторинг активности и системных ресурсов
- **Резервное копирование** - создание и скачивание бэкапов БД

---

## 🚀 Быстрый старт

### Установка

```bash
# Клонирование
git clone https://github.com/yourusername/yovpn-bot.git
cd yovpn-bot

# Автоматическая установка
chmod +x setup.sh
./setup.sh

# Настройка
nano .env
```

### Конфигурация

Минимальная конфигурация в `.env`:

```env
# Telegram
BOT_TOKEN=your_bot_token
ADMIN_TG_ID=7610842643

# База данных
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/yovpn

# Marzban
MARZBAN_API_URL=http://localhost:8000
MARZBAN_API_TOKEN=your_token

# Каналы
REQUIRED_CHANNEL=@yodevelop
SUPPORT_USERNAME=@yovpnsupbot
```

### Миграции

```bash
# Создание таблиц
alembic upgrade head
```

### Запуск

```bash
# Бот (текстовый режим)
python bot/main.py

# Админ-панель
uvicorn admin.main:app --host 0.0.0.0 --port 8080
```

---

## 📱 Использование бота

### Команды

- `/start` - Главное меню (проверка подписки + бонус)
- `/sub` - Моя подписка
- `/invite` - Реферальная программа

### Активация VPN (3 шага)

1. **Выбор платформы**
   - iOS (iPhone/iPad)
   - Android
   - Windows
   - macOS
   - Linux

2. **Установка приложения**
   - Рекомендации по приложению
   - Ссылки для скачивания
   - Альтернативные варианты

3. **Получение конфигурации**
   - Автоматическое создание в Marzban
   - Subscription URL
   - Инструкция по подключению

### Реферальная программа

1. Получить реферальную ссылку: `/invite`
2. Отправить друзьям
3. Получить **4 рубля (1 день VPN)** за регистрацию
4. Получать **до 10%** от пополнений рефералов

---

## 👨‍💼 Админ-панель

### URL: `http://your-server:8080/admin`

### Разделы

#### 1. Статистика

```
/admin/statistics              - Общая статистика
/admin/statistics/users        - Пользователи
/admin/statistics/finance      - Финансы
/admin/statistics/marzban      - Marzban
```

**Показывает:**
- Общее количество пользователей
- Активные пользователи
- Новые пользователи (за день/неделю/месяц)
- Активные подписки
- Доход по периодам
- Топ рефереров

#### 2. Пользователи

```
/admin/users                   - Список всех
/admin/users/{id}              - Детали пользователя
```

**Действия:**
- Просмотр информации
- Блокировка/разблокировка
- Изменение баланса
- Просмотр транзакций
- Просмотр подписок
- Удаление

#### 3. Управление балансом

```
/admin/balance                 - Главная
/admin/balance/add             - Пополнить
/admin/balance/withdraw        - Списать
/admin/balance/set             - Установить
/admin/balance/search          - Поиск
```

#### 4. Подписки

```
/admin/subscriptions           - Список
/admin/subscriptions/{id}      - Детали
```

**Действия:**
- Просмотр информации
- Активация/деактивация
- Фильтр по статусу

#### 5. Рассылка

```
/admin/broadcast               - Создать рассылку
```

**Возможности:**
- Текстовое сообщение
- Изображение
- Inline кнопки (внутри бота)
- Статистика отправки

#### 6. Marzban

```
/admin/marzban                 - Настройки
POST /admin/marzban/test       - Тест соединения
POST /admin/marzban/sync       - Синхронизация
/admin/marzban/users           - Пользователи
```

#### 7. Безопасность

```
/admin/security                - Обзор
/admin/security/logs           - Логи
/admin/security/monitoring     - Мониторинг
/admin/security/backups        - Резервные копии
POST /admin/security/backup    - Создать бэкап
```

**Мониторинг показывает:**
- CPU загрузка (%)
- RAM использование (GB)
- Disk использование (GB)
- Новые пользователи за час
- Транзакции за час

---

## 🗄️ База данных

### Обновленные модели

#### User (новые поля)

```python
referral_level        # Уровень в реферальной иерархии (0-5)
referral_earnings     # Заработок с рефералов (руб)
channel_subscribed    # Подписан ли на @yodevelop
channel_check_at      # Последняя проверка подписки
activation_step       # Текущий шаг активации (0-3)
selected_platform     # Выбранная платформа (ios/android/etc)
```

### Миграции

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Add referral fields"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

---

## 🔧 API Endpoints

### Статистика

```
GET  /admin/statistics              - Общая статистика
GET  /admin/statistics/users        - Статистика пользователей
GET  /admin/statistics/finance      - Финансовая статистика
GET  /admin/statistics/marzban      - Статистика Marzban
```

### Управление балансом

```
GET  /admin/balance                 - Главная
GET  /admin/balance/add             - Форма пополнения
POST /admin/balance/add             - Пополнить баланс
GET  /admin/balance/withdraw        - Форма списания
POST /admin/balance/withdraw        - Списать баланс
GET  /admin/balance/set             - Форма установки
POST /admin/balance/set             - Установить баланс
GET  /admin/balance/search          - Поиск пользователей
```

### Marzban

```
GET  /admin/marzban                 - Настройки
POST /admin/marzban/test            - Тест соединения
POST /admin/marzban/sync            - Синхронизация
GET  /admin/marzban/users           - Пользователи Marzban
```

### Безопасность

```
GET  /admin/security                - Обзор
GET  /admin/security/logs           - Просмотр логов
GET  /admin/security/monitoring     - Мониторинг системы
GET  /admin/security/backups        - Список бэкапов
POST /admin/security/backup         - Создать бэкап
GET  /admin/security/download-backup/{filename}  - Скачать бэкап
```

---

## 📊 Примеры использования

### Реферальная система

```python
from bot.handlers.referral_handler import ReferralHandler

# Регистрация реферала
await referral_handler.register_referral(
    user_id=новый_пользователь_id,
    referrer_id=реферер_id
)

# Получение дерева рефералов
tree = await referral_handler.get_referral_tree(user_id, max_level=5)

# Начисление бонусов при пополнении
await referral_handler.process_referral_deposit(user_id, amount=100.0)
```

### Проверка подписки на канал

```python
from bot.handlers.text_mode_handler import TextModeHandler

# Проверка подписки
is_subscribed = await text_handler.check_channel_subscription(user_id, bot)
```

### Синхронизация с Marzban

```http
POST /admin/marzban/sync
```

Ответ:
```json
{
  "success": true,
  "message": "✅ Синхронизировано: 45, ошибок: 0"
}
```

### Создание бэкапа

```http
POST /admin/security/backup
```

Ответ:
```json
{
  "success": true,
  "message": "✅ Резервная копия создана: yovpn_backup_20250124_153045.sql",
  "file": "backups/yovpn_backup_20250124_153045.sql"
}
```

---

## 🎨 Визуальные элементы

### Эмодзи в боте

```
💎 - Бонусы и премиум
🚀 - Активация
📊 - Статистика
💰 - Баланс
👥 - Рефералы
🛰️ - VPN подписка
✨ - Успех
❌ - Ошибка
⚠️ - Предупреждение
```

### Эмодзи в админ-панели

```
📊 - Статистика
👥 - Пользователи
💰 - Финансы
🛰️ - Подписки
📡 - Рассылка
🔧 - Настройки Marzban
🛡️ - Безопасность
```

---

## 📝 Changelog

### v2.0.0 (2025-01-24)

**Добавлено:**
- ✅ Текстовый режим бота с анимациями
- ✅ Проверка подписки на канал @yodevelop
- ✅ Реферальная система (5 уровней)
- ✅ Расширенная админ-панель (4 новых раздела)
- ✅ Статистика (общая, пользователи, финансы, Marzban)
- ✅ Управление балансом (пополнить, списать, установить)
- ✅ Настройки Marzban (тест, синхронизация)
- ✅ Безопасность (логи, мониторинг, бэкапы)

**Обновлено:**
- ✅ Модели БД (новые поля для рефералов и подписок)
- ✅ Админ-панель (новые разделы и функции)
- ✅ Документация (подробные инструкции)

---

## 🤝 Поддержка

- 💬 Техподдержка: [@yovpnsupbot](https://t.me/yovpnsupbot)
- 📢 Канал: [@yodevelop](https://t.me/yodevelop)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/yovpn-bot/issues)

---

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

**Сделано с ❤️ для сообщества VPN**

⭐ Поставьте звезду на GitHub если проект понравился!
