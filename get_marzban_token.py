#!/usr/bin/env python3
"""
Скрипт для получения токена администратора Marzban через API
"""

import requests
import json
import sys

def get_marzban_token():
    """Получить токен администратора Marzban"""
    print("=" * 60)
    print("ПОЛУЧЕНИЕ ТОКЕНА АДМИНИСТРАТОРА MARZBAN")
    print("=" * 60)
    
    # Настройки
    base_url = "https://alb-vpnprimex.duckdns.org"
    api_url = f"{base_url}/api"
    
    print(f"API URL: {api_url}")
    print()
    
    # Запрашиваем учетные данные
    username = input("Введите имя пользователя администратора: ").strip()
    password = input("Введите пароль администратора: ").strip()
    
    if not username or not password:
        print("❌ Имя пользователя и пароль не могут быть пустыми")
        return
    
    # Данные для авторизации
    auth_data = {
        "username": username,
        "password": password
    }
    
    print(f"\n1. Пытаемся авторизоваться как {username}...")
    
    try:
        # Отправляем запрос на авторизацию
        response = requests.post(
            f"{api_url}/admin/token",
            json=auth_data,
            timeout=30,
            verify=True
        )
        
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.text}")
        
        if response.status_code == 200:
            # Успешная авторизация
            token_data = response.json()
            access_token = token_data.get('access_token')
            
            if access_token:
                print(f"\n✅ Токен получен успешно!")
                print(f"🔑 Access Token: {access_token}")
                print(f"\n📋 Добавьте этот токен в .env файл:")
                print(f"MARZBAN_ADMIN_TOKEN={access_token}")
                
                # Проверяем токен
                print(f"\n2. Проверяем токен...")
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                
                test_response = requests.get(
                    f"{api_url}/system",
                    headers=headers,
                    timeout=30,
                    verify=True
                )
                
                print(f"   Статус: {test_response.status_code}")
                if test_response.status_code == 200:
                    print("   ✅ Токен работает корректно!")
                    system_info = test_response.json()
                    print(f"   📊 Версия Marzban: {system_info.get('version', 'Неизвестно')}")
                else:
                    print(f"   ❌ Токен не работает: {test_response.text}")
                
                return access_token
            else:
                print("❌ Токен не найден в ответе")
                return None
        else:
            print(f"❌ Ошибка авторизации: {response.status_code}")
            print(f"   Возможные причины:")
            print(f"   - Неправильное имя пользователя или пароль")
            print(f"   - У пользователя нет прав администратора")
            print(f"   - API недоступен")
            return None
            
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL ошибка: {e}")
        print("   Попробуем без проверки SSL...")
        
        try:
            response = requests.post(
                f"{api_url}/admin/token",
                json=auth_data,
                timeout=30,
                verify=False
            )
            
            print(f"   Статус (без SSL): {response.status_code}")
            print(f"   Ответ (без SSL): {response.text}")
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                
                if access_token:
                    print(f"\n✅ Токен получен успешно (без SSL)!")
                    print(f"🔑 Access Token: {access_token}")
                    return access_token
                else:
                    print("❌ Токен не найден в ответе")
                    return None
            else:
                print(f"❌ Ошибка авторизации (без SSL): {response.status_code}")
                return None
                
        except Exception as e2:
            print(f"❌ Ошибка запроса (без SSL): {e2}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
        return None

def update_env_file(token):
    """Обновить .env файл с новым токеном"""
    if not token:
        return
    
    print(f"\n3. Обновляем .env файл...")
    
    try:
        # Читаем текущий .env файл
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Обновляем MARZBAN_ADMIN_TOKEN
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('MARZBAN_ADMIN_TOKEN='):
                lines[i] = f'MARZBAN_ADMIN_TOKEN={token}\n'
                updated = True
                break
        
        # Если не найдено, добавляем новую строку
        if not updated:
            lines.append(f'MARZBAN_ADMIN_TOKEN={token}\n')
        
        # Записываем обновленный файл
        with open('.env', 'w') as f:
            f.writelines(lines)
        
        print("   ✅ .env файл обновлен")
        
    except Exception as e:
        print(f"   ❌ Ошибка обновления .env: {e}")

if __name__ == "__main__":
    token = get_marzban_token()
    if token:
        update_env_file(token)
        print(f"\n🎉 Готово! Теперь можно запустить бота:")
        print(f"   python3 main_improved.py")
    else:
        print(f"\n❌ Не удалось получить токен")
        print(f"🔧 Попробуйте получить токен через веб-интерфейс:")
        print(f"   https://alb-vpnprimex.duckdns.org")