#!/usr/bin/env python3
"""
Скрипт для обновления токена в .env файле
"""

import os
import sys

def update_token():
    """Обновить токен в .env файле"""
    print("=" * 60)
    print("ОБНОВЛЕНИЕ ТОКЕНА В .ENV ФАЙЛЕ")
    print("=" * 60)
    
    # Проверяем существование .env файла
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден")
        return False
    
    # Читаем текущий .env файл
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Ошибка чтения .env: {e}")
        return False
    
    # Показываем текущие значения
    print("Текущие значения в .env:")
    for line in lines:
        if line.strip() and '=' in line:
            key, value = line.split('=', 1)
            if 'TOKEN' in key or 'PASSWORD' in key:
                print(f"  {key}={value[:20]}..." if len(value.strip()) > 20 else f"  {key}={value.strip()}")
            else:
                print(f"  {key}={value.strip()}")
    
    print("\n" + "=" * 40)
    print("ВВЕДИТЕ НОВЫЕ ЗНАЧЕНИЯ")
    print("=" * 40)
    
    # Запрашиваем новые значения
    new_values = {}
    
    # Telegram Bot Token
    current_bot_token = None
    for line in lines:
        if line.startswith('USERBOT_TOKEN='):
            current_bot_token = line.split('=', 1)[1].strip()
            break
    
    if current_bot_token and current_bot_token != 'test_token':
        print(f"Текущий BOT_TOKEN: {current_bot_token[:20]}...")
        keep_bot = input("Оставить текущий BOT_TOKEN? (y/n): ").strip().lower()
        if keep_bot == 'y':
            new_values['USERBOT_TOKEN'] = current_bot_token
        else:
            new_values['USERBOT_TOKEN'] = input("Введите новый USERBOT_TOKEN: ").strip()
    else:
        new_values['USERBOT_TOKEN'] = input("Введите USERBOT_TOKEN: ").strip()
    
    # Marzban API URL
    new_values['MARZBAN_API_URL'] = input("Введите MARZBAN_API_URL (по умолчанию: https://alb-vpnprimex.duckdns.org/api): ").strip()
    if not new_values['MARZBAN_API_URL']:
        new_values['MARZBAN_API_URL'] = 'https://alb-vpnprimex.duckdns.org/api'
    
    # Marzban Admin Token
    new_values['MARZBAN_ADMIN_TOKEN'] = input("Введите MARZBAN_ADMIN_TOKEN: ").strip()
    
    # Database Password
    current_db_password = None
    for line in lines:
        if line.startswith('DB_PASSWORD='):
            current_db_password = line.split('=', 1)[1].strip()
            break
    
    if current_db_password and current_db_password != 'test_password':
        print(f"Текущий DB_PASSWORD: {current_db_password[:10]}...")
        keep_db = input("Оставить текущий DB_PASSWORD? (y/n): ").strip().lower()
        if keep_db == 'y':
            new_values['DB_PASSWORD'] = current_db_password
        else:
            new_values['DB_PASSWORD'] = input("Введите новый DB_PASSWORD: ").strip()
    else:
        new_values['DB_PASSWORD'] = input("Введите DB_PASSWORD: ").strip()
    
    # Обновляем файл
    print(f"\nОбновляем .env файл...")
    
    try:
        # Создаем новые строки
        new_lines = []
        for line in lines:
            if line.strip() and '=' in line:
                key = line.split('=', 1)[0]
                if key in new_values:
                    new_lines.append(f"{key}={new_values[key]}\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # Записываем обновленный файл
        with open('.env', 'w') as f:
            f.writelines(new_lines)
        
        print("✅ .env файл обновлен")
        
        # Показываем обновленные значения
        print("\nОбновленные значения:")
        for key, value in new_values.items():
            if 'TOKEN' in key or 'PASSWORD' in key:
                print(f"  {key}={value[:20]}..." if len(value) > 20 else f"  {key}={value}")
            else:
                print(f"  {key}={value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления .env: {e}")
        return False

if __name__ == "__main__":
    if update_token():
        print(f"\n🎉 Готово! Теперь можно проверить токен:")
        print(f"   python3 check_marzban_token.py")
        print(f"\nИ запустить бота:")
        print(f"   python3 main_improved.py")
    else:
        print(f"\n❌ Не удалось обновить токен")
        print(f"🔧 Попробуйте отредактировать .env файл вручную:")
        print(f"   nano .env")