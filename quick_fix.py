#!/usr/bin/env python3
"""
Быстрое исправление конфигурации
"""

import os
import sys

def main():
    print("🔧 Быстрое исправление конфигурации YoVPN бота")
    print("=" * 60)
    
    # Проверяем текущий .env
    env_file = '.env'
    if not os.path.exists(env_file):
        print("❌ Файл .env не найден!")
        return False
    
    print("📄 Текущий .env файл:")
    with open(env_file, 'r') as f:
        content = f.read()
        print(content)
    
    print("\n" + "=" * 60)
    print("🚨 ПРОБЛЕМА: В .env файле установлены placeholder значения")
    print("=" * 60)
    
    print("\n📋 ЧТО НУЖНО СДЕЛАТЬ:")
    print("1. Получите токен бота у @BotFather в Telegram")
    print("2. Получите токен Marzban из Swagger UI")
    print("3. Обновите .env файл с реальными значениями")
    
    print("\n🔧 БЫСТРОЕ РЕШЕНИЕ:")
    print("1. Скопируйте .env.sample в .env:")
    print("   cp .env.sample .env")
    print("2. Отредактируйте .env файл:")
    print("   nano .env")
    print("3. Замените placeholder значения на реальные токены")
    
    print("\n📖 ПОДРОБНАЯ ИНСТРУКЦИЯ:")
    print("   Смотрите файл SETUP_INSTRUCTIONS.md")
    
    print("\n🔍 ПРОВЕРКА ПОСЛЕ ИСПРАВЛЕНИЯ:")
    print("   python3 check_and_fix_config.py")
    
    print("\n🚀 ЗАПУСК БОТА:")
    print("   python3 main_improved.py")
    
    return True

if __name__ == "__main__":
    main()