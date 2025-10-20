#!/usr/bin/env python3
"""
Скрипт для установки и настройки инструментов безопасности
"""

import subprocess
import sys
import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_command(command: str, description: str) -> bool:
    """Выполнить команду и вернуть результат"""
    logger.info(f"Выполняю: {description}")
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"✅ {description} - успешно")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} - ошибка: {e.stderr}")
        return False

def install_python_packages():
    """Установка Python пакетов для безопасности"""
    packages = [
        "bandit",
        "safety", 
        "semgrep",
        "pip-audit",
        "black",
        "isort",
        "flake8",
        "mypy",
        "pre-commit"
    ]
    
    logger.info("Устанавливаю пакеты безопасности...")
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Установка {package}"):
            logger.warning(f"Не удалось установить {package}")

def setup_pre_commit_hooks():
    """Настройка pre-commit хуков"""
    logger.info("Настраиваю pre-commit хуки...")
    
    # Создаем .pre-commit-config.yaml
    pre_commit_config = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements
      - id: check-docstring-first

  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-Pillow]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/', '-f', 'json', '-o', 'bandit-report.json']

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
"""
    
    with open('.pre-commit-config.yaml', 'w') as f:
        f.write(pre_commit_config)
    
    # Устанавливаем pre-commit хуки
    run_command("pre-commit install", "Установка pre-commit хуков")

def create_security_scripts():
    """Создание скриптов безопасности"""
    
    # Скрипт для проверки безопасности
    security_check_script = """#!/bin/bash
# Скрипт проверки безопасности

echo "🔍 Запуск проверки безопасности..."

# Проверка зависимостей
echo "📦 Проверка уязвимостей в зависимостях..."
pip-audit --desc --format=json --output=audit-report.json

# Проверка безопасности кода
echo "🛡️ Проверка безопасности кода..."
bandit -r src/ -f json -o bandit-report.json

# Проверка с помощью semgrep
echo "🔎 Сканирование кода с помощью semgrep..."
semgrep --config=auto src/ --json --output=semgrep-report.json

# Проверка секретов
echo "🔐 Проверка секретов..."
detect-secrets scan --baseline .secrets.baseline

echo "✅ Проверка безопасности завершена"
echo "📊 Отчеты сохранены в:"
echo "  - audit-report.json (зависимости)"
echo "  - bandit-report.json (безопасность кода)"
echo "  - semgrep-report.json (семантическое сканирование)"
"""
    
    with open('security_check.sh', 'w') as f:
        f.write(security_check_script)
    
    os.chmod('security_check.sh', 0o755)
    
    # Скрипт для обновления зависимостей
    update_deps_script = """#!/bin/bash
# Скрипт обновления зависимостей

echo "🔄 Обновление зависимостей..."

# Обновление pip
pip install --upgrade pip

# Обновление зависимостей
pip install --upgrade -r requirements_async.txt

# Проверка уязвимостей
echo "🔍 Проверка уязвимостей..."
pip-audit

echo "✅ Обновление завершено"
"""
    
    with open('update_dependencies.sh', 'w') as f:
        f.write(update_deps_script)
    
    os.chmod('update_dependencies.sh', 0o755)

def create_dockerfile_security():
    """Создание безопасного Dockerfile"""
    dockerfile_content = """
# Безопасный Dockerfile для YoVPN бота
FROM python:3.11-slim

# Создаем пользователя без root привилегий
RUN groupadd -r botuser && useradd -r -g botuser botuser

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \\
    --no-install-recommends \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python зависимости
COPY requirements_async.txt .
RUN pip install --no-cache-dir -r requirements_async.txt

# Копируем код приложения
COPY src/ /app/src/
COPY *.py /app/

# Устанавливаем права доступа
RUN chown -R botuser:botuser /app
RUN chmod -R 755 /app

# Переключаемся на непривилегированного пользователя
USER botuser

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт для метрик
EXPOSE 8000

# Запускаем приложение
CMD ["python", "-m", "src.bot.async_bot"]
"""
    
    with open('Dockerfile.secure', 'w') as f:
        f.write(dockerfile_content)

def create_docker_compose_security():
    """Создание безопасного docker-compose"""
    compose_content = """
version: '3.8'

services:
  yovpn-bot:
    build:
      context: .
      dockerfile: Dockerfile.secure
    container_name: yovpn-bot
    restart: unless-stopped
    environment:
      - USERBOT_TOKEN=${USERBOT_TOKEN}
      - MARZBAN_API_URL=${MARZBAN_API_URL}
      - MARZBAN_ADMIN_TOKEN=${MARZBAN_ADMIN_TOKEN}
      - SENTRY_DSN=${SENTRY_DSN}
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./data:/app/data:rw
      - ./logs:/app/logs:rw
    ports:
      - "8000:8000"  # Prometheus метрики
    depends_on:
      - redis
    networks:
      - bot-network
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=100m

  redis:
    image: redis:7-alpine
    container_name: yovpn-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - bot-network
    security_opt:
      - no-new-privileges:true

  prometheus:
    image: prom/prometheus:latest
    container_name: yovpn-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    networks:
      - bot-network

  grafana:
    image: grafana/grafana:latest
    container_name: yovpn-grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - bot-network

volumes:
  redis-data:
  prometheus-data:
  grafana-data:

networks:
  bot-network:
    driver: bridge
"""
    
    with open('docker-compose.secure.yml', 'w') as f:
        f.write(compose_content)

def create_monitoring_config():
    """Создание конфигурации мониторинга"""
    os.makedirs('monitoring', exist_ok=True)
    
    # Prometheus конфигурация
    prometheus_config = """
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

scrape_configs:
  - job_name: 'yovpn-bot'
    static_configs:
      - targets: ['yovpn-bot:8000']
    scrape_interval: 5s
    metrics_path: /metrics

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 30s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []
"""
    
    with open('monitoring/prometheus.yml', 'w') as f:
        f.write(prometheus_config)
    
    # Grafana дашборд
    os.makedirs('monitoring/grafana/dashboards', exist_ok=True)
    
    dashboard_config = """
{
  "dashboard": {
    "title": "YoVPN Bot Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(bot_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Error Rate", 
        "type": "graph",
        "targets": [
          {
            "expr": "rate(bot_errors_total[5m])",
            "legendFormat": "{{error_type}}"
          }
        ]
      },
      {
        "title": "Active Users",
        "type": "singlestat",
        "targets": [
          {
            "expr": "bot_active_users"
          }
        ]
      }
    ]
  }
}
"""
    
    with open('monitoring/grafana/dashboards/bot-dashboard.json', 'w') as f:
        f.write(dashboard_config)

def main():
    """Главная функция"""
    logger.info("🔧 Настройка инструментов безопасности...")
    
    # Устанавливаем Python пакеты
    install_python_packages()
    
    # Настраиваем pre-commit хуки
    setup_pre_commit_hooks()
    
    # Создаем скрипты безопасности
    create_security_scripts()
    
    # Создаем безопасные Docker файлы
    create_dockerfile_security()
    create_docker_compose_security()
    
    # Создаем конфигурацию мониторинга
    create_monitoring_config()
    
    logger.info("✅ Настройка инструментов безопасности завершена!")
    logger.info("📋 Следующие шаги:")
    logger.info("1. Запустите: ./security_check.sh")
    logger.info("2. Настройте pre-commit: pre-commit run --all-files")
    logger.info("3. Обновите .env с новыми переменными")
    logger.info("4. Запустите: docker-compose -f docker-compose.secure.yml up")

if __name__ == "__main__":
    main()