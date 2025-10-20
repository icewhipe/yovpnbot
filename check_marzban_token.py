#!/usr/bin/env python3
"""
Скрипт для проверки токена администратора Marzban
"""

import requests
import json
import sys

def check_marzban_token():
    """Проверить токен администратора Marzban"""
    print("=" * 60)
    print("ПРОВЕРКА ТОКЕНА АДМИНИСТРАТОРА MARZBAN")
    print("=" * 60)
    
    # Настройки
    base_url = "https://alb-vpnprimex.duckdns.org"
    api_url = f"{base_url}/api"
    
    print(f"API URL: {api_url}")
    
    # Получаем токен из .env файла
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        token = None
        for line in content.strip().split('\n'):
            if line.startswith('MARZBAN_ADMIN_TOKEN='):
                token = line.split('=', 1)[1].strip()
                break
        
        if not token:
            print("❌ Токен не найден в .env файле")
            return False
        
        print(f"🔑 Токен: {token[:20]}...")
        
    except FileNotFoundError:
        print("❌ Файл .env не найден")
        return False
    except Exception as e:
        print(f"❌ Ошибка чтения .env: {e}")
        return False
    
    # Проверяем токен
    print(f"\n1. Проверяем токен...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'YOVPN-Bot/1.0'
    }
    
    try:
        # Проверяем системную информацию
        response = requests.get(
            f"{api_url}/system",
            headers=headers,
            timeout=30,
            verify=True
        )
        
        print(f"   Статус: {response.status_code}")
        print(f"   Ответ: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Токен работает корректно!")
            
            try:
                system_info = response.json()
                print(f"   📊 Версия Marzban: {system_info.get('version', 'Неизвестно')}")
                print(f"   📊 Статус: {system_info.get('status', 'Неизвестно')}")
            except:
                pass
            
            # Проверяем права администратора
            print(f"\n2. Проверяем права администратора...")
            
            try:
                # Пробуем получить список пользователей (требует права администратора)
                users_response = requests.get(
                    f"{api_url}/users",
                    headers=headers,
                    timeout=30,
                    verify=True
                )
                
                print(f"   Статус: {users_response.status_code}")
                
                if users_response.status_code == 200:
                    print("   ✅ Права администратора подтверждены!")
                    users_data = users_response.json()
                    print(f"   📊 Количество пользователей: {len(users_data) if isinstance(users_data, list) else 'Неизвестно'}")
                elif users_response.status_code == 403:
                    print("   ❌ Недостаточно прав (требуются права администратора)")
                    return False
                else:
                    print(f"   ⚠️ Неожиданный статус: {users_response.status_code}")
                
            except Exception as e:
                print(f"   ⚠️ Ошибка проверки прав: {e}")
            
            return True
            
        elif response.status_code == 401:
            print("   ❌ Токен недействителен или истек")
            print("   🔧 Решение: Получите новый токен через веб-интерфейс")
            return False
        elif response.status_code == 403:
            print("   ❌ Доступ запрещен")
            print("   🔧 Решение: Убедитесь, что у токена есть права администратора")
            return False
        else:
            print(f"   ⚠️ Неожиданный статус: {response.status_code}")
            return False
            
    except requests.exceptions.SSLError as e:
        print(f"   ⚠️ SSL ошибка: {e}")
        print("   Попробуем без проверки SSL...")
        
        try:
            response = requests.get(
                f"{api_url}/system",
                headers=headers,
                timeout=30,
                verify=False
            )
            
            print(f"   Статус (без SSL): {response.status_code}")
            print(f"   Ответ (без SSL): {response.text}")
            
            if response.status_code == 200:
                print("   ✅ Токен работает корректно (без SSL)!")
                return True
            elif response.status_code == 401:
                print("   ❌ Токен недействителен или истек (без SSL)")
                return False
            else:
                print(f"   ⚠️ Неожиданный статус (без SSL): {response.status_code}")
                return False
                
        except Exception as e2:
            print(f"   ❌ Ошибка запроса (без SSL): {e2}")
            return False
            
    except Exception as e:
        print(f"   ❌ Ошибка запроса: {e}")
        return False

if __name__ == "__main__":
    if check_marzban_token():
        print(f"\n🎉 Токен работает! Можно запускать бота:")
        print(f"   python3 main_improved.py")
    else:
        print(f"\n❌ Токен не работает")
        print(f"🔧 Получите новый токен:")
        print(f"   python3 get_marzban_token.py")