#!/usr/bin/env python3
"""
Скрипт для обновления конфигурации бота
"""

import os
import sys
from pathlib import Path

def update_env_file(bot_token=None, marzban_token=None):
    """Обновить .env файл"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ Файл .env не найден!")
        return False
    
    # Читаем текущий файл
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Обновляем токены
    updated_lines = []
    for line in lines:
        if line.startswith('USERBOT_TOKEN=') and bot_token:
            updated_lines.append(f'USERBOT_TOKEN={bot_token}\n')
        elif line.startswith('MARZBAN_ADMIN_TOKEN=') and marzban_token:
            updated_lines.append(f'MARZBAN_ADMIN_TOKEN={marzban_token}\n')
        else:
            updated_lines.append(line)
    
    # Записываем обновленный файл
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("✅ .env файл обновлен")
    return True

def interactive_update():
    """Интерактивное обновление конфигурации"""
    print("🔧 Обновление конфигурации YoVPN бота")
    print("=" * 50)
    
    # Проверяем текущие значения
    try:
        from src.config import config
        print(f"Текущий токен бота: {config.BOT_TOKEN[:10]}...")
        print(f"Текущий токен Marzban: {config.MARZBAN_ADMIN_TOKEN[:10]}...")
    except Exception as e:
        print(f"Ошибка чтения конфигурации: {e}")
        return False
    
    print("\nВведите новые значения (нажмите Enter чтобы пропустить):")
    
    # Запрашиваем токен бота
    bot_token = input("\n🤖 Токен Telegram бота: ").strip()
    if not bot_token:
        bot_token = None
        print("   Пропущено")
    
    # Запрашиваем токен Marzban
    marzban_token = input("🌐 Токен Marzban администратора: ").strip()
    if not marzban_token:
        marzban_token = None
        print("   Пропущено")
    
    # Обновляем файл
    if bot_token or marzban_token:
        if update_env_file(bot_token, marzban_token):
            print("\n✅ Конфигурация обновлена!")
            
            # Проверяем обновленную конфигурацию
            print("\n🔍 Проверяем обновленную конфигурацию...")
            try:
                # Перезагружаем модуль конфигурации
                import importlib
                import src.config
                importlib.reload(src.config)
                
                from src.config import config
                print(f"   Токен бота: {config.BOT_TOKEN[:10]}...")
                print(f"   Токен Marzban: {config.MARZBAN_ADMIN_TOKEN[:10]}...")
                
                return True
            except Exception as e:
                print(f"   Ошибка проверки: {e}")
                return False
        else:
            return False
    else:
        print("❌ Нечего обновлять")
        return False

def main():
    """Главная функция"""
    if len(sys.argv) > 1:
        # Неинтерактивный режим
        if sys.argv[1] == '--help':
            print("Использование:")
            print("  python3 update_config.py                    # Интерактивный режим")
            print("  python3 update_config.py --help             # Показать справку")
            return True
        else:
            print("❌ Неизвестный аргумент. Используйте --help для справки")
            return False
    else:
        # Интерактивный режим
        return interactive_update()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)