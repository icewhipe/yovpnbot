#!/usr/bin/env python3
"""
Тестовый скрипт для проверки подключения к реальному Marzban API
"""

import os
import sys
import logging
import requests

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_marzban_connection():
    """Тестируем подключение к реальному Marzban API"""
    print("=" * 60)
    print("ТЕСТ ПОДКЛЮЧЕНИЯ К РЕАЛЬНОМУ MARZBAN API")
    print("=" * 60)
    
    # Получаем значения из переменных окружения
    api_url = os.getenv('MARZBAN_API_URL', 'https://test.com/api')
    admin_token = os.getenv('MARZBAN_ADMIN_TOKEN', 'test_token')
    
    print(f"API URL: {api_url}")
    print(f"Admin Token: {admin_token[:20]}..." if admin_token else "НЕ УСТАНОВЛЕН")
    print()
    
    # Проверяем доступность сервера
    print("1. Проверяем доступность сервера...")
    try:
        # Убираем /api из URL для проверки основного домена
        base_url = api_url.replace('/api', '')
        response = requests.get(base_url, timeout=10, verify=True)
        print(f"   ✅ Сервер доступен: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"   ⚠️ SSL ошибка: {e}")
        print("   Попробуем без проверки SSL...")
        try:
            response = requests.get(base_url, timeout=10, verify=False)
            print(f"   ✅ Сервер доступен (без SSL): {response.status_code}")
        except Exception as e2:
            print(f"   ❌ Сервер недоступен: {e2}")
            return
    except Exception as e:
        print(f"   ❌ Сервер недоступен: {e}")
        return
    
    # Проверяем API endpoint
    print("\n2. Проверяем API endpoint...")
    try:
        response = requests.get(f"{api_url}/system", timeout=10, verify=True)
        print(f"   ✅ API endpoint доступен: {response.status_code}")
        if response.status_code == 200:
            print(f"   📄 Ответ: {response.text[:200]}...")
    except requests.exceptions.SSLError as e:
        print(f"   ⚠️ SSL ошибка: {e}")
        print("   Попробуем без проверки SSL...")
        try:
            response = requests.get(f"{api_url}/system", timeout=10, verify=False)
            print(f"   ✅ API endpoint доступен (без SSL): {response.status_code}")
            if response.status_code == 200:
                print(f"   📄 Ответ: {response.text[:200]}...")
        except Exception as e2:
            print(f"   ❌ API endpoint недоступен: {e2}")
            return
    except Exception as e:
        print(f"   ❌ API endpoint недоступен: {e}")
        return
    
    # Проверяем авторизацию
    print("\n3. Проверяем авторизацию...")
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'YOVPN-Bot/1.0'
    }
    
    try:
        response = requests.get(f"{api_url}/system", headers=headers, timeout=10, verify=True)
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Авторизация успешна!")
            try:
                data = response.json()
                print(f"   📊 Версия Marzban: {data.get('version', 'Неизвестно')}")
                print(f"   📊 Статус: {data.get('status', 'Неизвестно')}")
            except:
                pass
        elif response.status_code == 401:
            print("   ❌ Ошибка авторизации!")
            print("   🔧 Возможные причины:")
            print("      - Неправильный токен")
            print("      - Токен истек")
            print("      - Неправильный формат токена")
            print("      - У токена нет прав администратора")
        elif response.status_code == 403:
            print("   ❌ Доступ запрещен!")
            print("   🔧 Возможные причины:")
            print("      - У токена нет прав администратора")
            print("      - IP адрес заблокирован")
        else:
            print(f"   ⚠️ Неожиданный статус: {response.status_code}")
            
    except requests.exceptions.SSLError as e:
        print(f"   ⚠️ SSL ошибка: {e}")
        print("   Попробуем без проверки SSL...")
        try:
            response = requests.get(f"{api_url}/system", headers=headers, timeout=10, verify=False)
            print(f"   Статус (без SSL): {response.status_code}")
            print(f"   Ответ (без SSL): {response.text}")
            
            if response.status_code == 200:
                print("   ✅ Авторизация успешна (без SSL)!")
            elif response.status_code == 401:
                print("   ❌ Ошибка авторизации (без SSL)!")
            else:
                print(f"   ⚠️ Неожиданный статус (без SSL): {response.status_code}")
        except Exception as e2:
            print(f"   ❌ Ошибка запроса (без SSL): {e2}")
    except Exception as e:
        print(f"   ❌ Ошибка запроса: {e}")
    
    print("\n" + "=" * 60)
    print("РЕКОМЕНДАЦИИ:")
    print("=" * 60)
    
    if admin_token == 'test_token':
        print("1. ❌ Используется тестовый токен")
        print("   🔧 Решение: Установите реальный токен в переменную MARZBAN_ADMIN_TOKEN")
    else:
        print("1. ✅ Используется реальный токен")
    
    if api_url == 'https://test.com/api':
        print("2. ❌ Используется тестовый URL")
        print("   🔧 Решение: Установите реальный URL в переменную MARZBAN_API_URL")
    else:
        print("2. ✅ Используется реальный URL")
    
    print("\n3. 🔧 Как получить правильный токен:")
    print("   - Войдите в панель Marzban")
    print("   - Перейдите в Settings → API")
    print("   - Скопируйте Admin Token")
    print("   - Убедитесь, что у токена есть права администратора")
    
    print("\n4. 🔧 Как установить переменные окружения:")
    print("   export MARZBAN_API_URL='https://your-domain.com/api'")
    print("   export MARZBAN_ADMIN_TOKEN='your_actual_token_here'")
    print("   # Или создайте .env файл с этими значениями")

if __name__ == "__main__":
    test_marzban_connection()