#!/usr/bin/env python3
"""
Скрипт для проверки всех возможных источников переменных окружения
"""

import os
import sys
import subprocess

def check_all_env():
    """Проверяем все возможные источники переменных окружения"""
    print("=" * 60)
    print("ПРОВЕРКА ВСЕХ ИСТОЧНИКОВ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
    print("=" * 60)
    
    # 1. Переменные окружения текущего процесса
    print("1. Переменные окружения текущего процесса:")
    env_vars = ['USERBOT_TOKEN', 'MARZBAN_API_URL', 'MARZBAN_ADMIN_TOKEN', 'DB_PASSWORD']
    for var in env_vars:
        value = os.getenv(var, 'НЕ УСТАНОВЛЕНА')
        if 'TOKEN' in var or 'PASSWORD' in var:
            print(f"   {var}: {value[:20]}..." if value != 'НЕ УСТАНОВЛЕНА' else f"   {var}: {value}")
        else:
            print(f"   {var}: {value}")
    
    # 2. Проверяем файлы .env
    print("\n2. Файлы .env:")
    env_files = ['.env', '.env.local', '.env.production', '.env.development']
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"   ✅ {env_file} существует")
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    print(f"      Содержимое:")
                    for line in content.strip().split('\n'):
                        if line.strip() and '=' in line:
                            key, value = line.split('=', 1)
                            if 'TOKEN' in key or 'PASSWORD' in key:
                                print(f"        {key}={value[:20]}..." if len(value) > 20 else f"        {key}={value}")
                            else:
                                print(f"        {key}={value}")
            except Exception as e:
                print(f"      Ошибка чтения: {e}")
        else:
            print(f"   ❌ {env_file} не существует")
    
    # 3. Проверяем переменные окружения через env команду
    print("\n3. Переменные окружения через env команду:")
    try:
        result = subprocess.run(['env'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            env_output = result.stdout
            for var in env_vars:
                lines = [line for line in env_output.split('\n') if line.startswith(f"{var}=")]
                if lines:
                    for line in lines:
                        key, value = line.split('=', 1)
                        if 'TOKEN' in key or 'PASSWORD' in key:
                            print(f"   {key}={value[:20]}..." if len(value) > 20 else f"   {key}={value}")
                        else:
                            print(f"   {key}={value}")
                else:
                    print(f"   {var}: НЕ УСТАНОВЛЕНА")
        else:
            print(f"   Ошибка выполнения env: {result.stderr}")
    except Exception as e:
        print(f"   Ошибка выполнения env: {e}")
    
    # 4. Проверяем переменные окружения через printenv
    print("\n4. Переменные окружения через printenv:")
    try:
        for var in env_vars:
            result = subprocess.run(['printenv', var], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                value = result.stdout.strip()
                if 'TOKEN' in var or 'PASSWORD' in var:
                    print(f"   {var}: {value[:20]}..." if len(value) > 20 else f"   {var}: {value}")
                else:
                    print(f"   {var}: {value}")
            else:
                print(f"   {var}: НЕ УСТАНОВЛЕНА")
    except Exception as e:
        print(f"   Ошибка выполнения printenv: {e}")
    
    # 5. Проверяем переменные окружения через getenv
    print("\n5. Переменные окружения через os.getenv:")
    for var in env_vars:
        value = os.getenv(var, 'НЕ УСТАНОВЛЕНА')
        if 'TOKEN' in var or 'PASSWORD' in var:
            print(f"   {var}: {value[:20]}..." if value != 'НЕ УСТАНОВЛЕНА' else f"   {var}: {value}")
        else:
            print(f"   {var}: {value}")
    
    # 6. Проверяем переменные окружения через environ
    print("\n6. Переменные окружения через os.environ:")
    for var in env_vars:
        if var in os.environ:
            value = os.environ[var]
            if 'TOKEN' in var or 'PASSWORD' in var:
                print(f"   {var}: {value[:20]}..." if len(value) > 20 else f"   {var}: {value}")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: НЕ УСТАНОВЛЕНА")
    
    print("\n" + "=" * 60)
    print("ЗАКЛЮЧЕНИЕ:")
    print("=" * 60)
    
    # Анализируем результаты
    real_values_found = False
    for var in env_vars:
        value = os.getenv(var, 'НЕ УСТАНОВЛЕНА')
        if value != 'НЕ УСТАНОВЛЕНА' and value not in ['test_token', 'https://test.com/api', 'test_password']:
            real_values_found = True
            break
    
    if real_values_found:
        print("✅ Найдены реальные значения переменных окружения")
        print("🔧 Рекомендация: Используйте эти значения для настройки бота")
    else:
        print("❌ Реальные значения переменных окружения не найдены")
        print("🔧 Рекомендация: Установите переменные окружения или настройте .env файл")
    
    print("\n📋 Следующие шаги:")
    print("1. Если найдены реальные значения - используйте их")
    print("2. Если не найдены - настройте .env файл с реальными значениями")
    print("3. Запустите бота с правильной конфигурацией")

if __name__ == "__main__":
    check_all_env()