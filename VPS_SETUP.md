# Инструкция по запуску YOVPN Bot на VPS

## 🚀 Быстрый старт

### 1. Подключение к VPS
```bash
ssh root@your-vps-ip
```

### 2. Клонирование репозитория
```bash
# Клонируем репозиторий
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Переключаемся на нужную ветку
git checkout cursor/review-and-improve-yovpn-telegram-bot-40ee
```

### 3. Установка зависимостей
```bash
# Обновляем систему
apt update && apt upgrade -y

# Устанавливаем Python и pip
apt install python3 python3-pip -y

# Устанавливаем зависимости проекта
pip3 install -r requirements.txt
```

### 4. Настройка конфигурации
```bash
# Копируем пример конфигурации
cp .env.example .env

# Редактируем конфигурацию
nano .env
```

**Содержимое .env файла:**
```env
# Telegram Bot Configuration
USERBOT_TOKEN=your_actual_telegram_bot_token_here

# Marzban API Configuration
MARZBAN_API_URL=https://your-marzban-api-url.com/api
MARZBAN_ADMIN_TOKEN=your_actual_marzban_admin_token_here

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=marzban
DB_USER=marzban
DB_PASSWORD=your_secure_database_password_here

# Data file path (relative to project root)
DATA_FILE=data.json
```

### 5. Запуск бота

#### Вариант 1: Прямой запуск
```bash
# Запускаем бота
python3 main_improved.py
```

#### Вариант 2: Запуск в фоне с nohup
```bash
# Запускаем в фоне
nohup python3 main_improved.py > bot.log 2>&1 &

# Проверяем, что бот запущен
ps aux | grep python3

# Смотрим логи
tail -f bot.log
```

#### Вариант 3: Запуск через systemd (рекомендуется)
```bash
# Создаем systemd сервис
cat > /etc/systemd/system/yovpn-bot.service << EOF
[Unit]
Description=YOVPN Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/yovpnbot
ExecStart=/usr/bin/python3 main_improved.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезагружаем systemd
systemctl daemon-reload

# Включаем автозапуск
systemctl enable yovpn-bot

# Запускаем сервис
systemctl start yovpn-bot

# Проверяем статус
systemctl status yovpn-bot

# Смотрим логи
journalctl -u yovpn-bot -f
```

## 🔧 Настройка для продакшена

### 1. Настройка файрвола
```bash
# Открываем необходимые порты
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 2. Настройка SSL для Marzban API
```bash
# Если у вас самоподписанный сертификат, добавьте его в доверенные
# Или отключите SSL проверку в коде (НЕ РЕКОМЕНДУЕТСЯ)
```

### 3. Настройка логирования
```bash
# Создаем директорию для логов
mkdir -p /var/log/yovpn-bot

# Настраиваем ротацию логов
cat > /etc/logrotate.d/yovpn-bot << EOF
/var/log/yovpn-bot/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
EOF
```

## 🐳 Запуск через Docker (альтернатива)

### 1. Установка Docker
```bash
# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Устанавливаем Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 2. Запуск через Docker Compose
```bash
# Запускаем все сервисы
docker-compose up -d

# Проверяем статус
docker-compose ps

# Смотрим логи
docker-compose logs -f yovpn-bot
```

## 📊 Мониторинг и обслуживание

### 1. Проверка статуса
```bash
# Проверяем, что бот работает
ps aux | grep python3

# Проверяем логи
tail -f bot.log

# Проверяем использование ресурсов
htop
```

### 2. Перезапуск бота
```bash
# Если запущен через systemd
systemctl restart yovpn-bot

# Если запущен через nohup
pkill -f "python3 main_improved.py"
nohup python3 main_improved.py > bot.log 2>&1 &

# Если запущен через Docker
docker-compose restart yovpn-bot
```

### 3. Обновление бота
```bash
# Останавливаем бота
systemctl stop yovpn-bot

# Обновляем код
git pull origin cursor/review-and-improve-yovpn-telegram-bot-40ee

# Устанавливаем новые зависимости (если есть)
pip3 install -r requirements.txt

# Запускаем бота
systemctl start yovpn-bot
```

## 🚨 Устранение неполадок

### Проблема: "ModuleNotFoundError: No module named 'decouple'"
**Решение:**
```bash
pip3 install -r requirements.txt
```

### Проблема: "No such file or directory: 'data.json'"
**Решение:**
```bash
# Создаем файл данных
touch data.json
echo '{}' > data.json
```

### Проблема: "SSL: CERTIFICATE_VERIFY_FAILED"
**Решение:**
```bash
# Проверьте, что Marzban API использует валидный SSL сертификат
# Или временно отключите SSL проверку в коде (НЕ РЕКОМЕНДУЕТСЯ)
```

### Проблема: "Conflict: terminated by other getUpdates request"
**Решение:**
```bash
# Остановите все экземпляры бота
pkill -f "python3 main_improved.py"

# Запустите заново
python3 main_improved.py
```

## 📈 Оптимизация производительности

### 1. Настройка Python
```bash
# Устанавливаем переменные окружения для оптимизации
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
```

### 2. Мониторинг ресурсов
```bash
# Устанавливаем htop для мониторинга
apt install htop -y

# Запускаем мониторинг
htop
```

### 3. Настройка логирования
```bash
# Настраиваем уровень логирования в коде
# Измените level=logging.INFO на level=logging.WARNING для продакшена
```

## 🔒 Безопасность

### 1. Настройка файрвола
```bash
# Блокируем все входящие соединения кроме необходимых
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 2. Настройка SSH
```bash
# Отключаем root логин
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Перезапускаем SSH
systemctl restart ssh
```

### 3. Регулярные обновления
```bash
# Настраиваем автоматические обновления безопасности
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `tail -f bot.log`
2. Проверьте статус: `systemctl status yovpn-bot`
3. Проверьте конфигурацию: `cat .env`
4. Обратитесь к документации: `README.md`

## ✅ Чек-лист запуска

- [ ] VPS настроен и доступен
- [ ] Python 3 и pip установлены
- [ ] Зависимости установлены
- [ ] Конфигурация настроена
- [ ] Бот запущен и работает
- [ ] Логирование настроено
- [ ] Мониторинг настроен
- [ ] Безопасность настроена