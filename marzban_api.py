#!/usr/bin/env python3
"""
API для работы с Marzban
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import logging
import urllib3

# Отключаем SSL предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class MarzbanAPI:
    def __init__(self, api_url: str, admin_token: str = None, timeout: int = 10):
        self.api_url = api_url.rstrip('/')
        self.admin_token = admin_token
        self.timeout = timeout
        self.session = requests.Session()
        
        # Отключаем SSL проверку для локального API
        self.session.verify = False
        
        if admin_token:
            self.session.headers.update({
                'Authorization': f'Bearer {admin_token}',
                'Content-Type': 'application/json'
            })
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Получить пользователя по username"""
        # Убираем @ из username если есть
        clean_username = username.lstrip('@')
        logger.info(f"Ищем пользователя в Marzban: {clean_username}")
        
        try:
            response = self.session.get(
                f"{self.api_url}/user/{clean_username}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Найден пользователь {clean_username} в Marzban")
                return user_data
            elif response.status_code == 404:
                logger.info(f"Пользователь {clean_username} не найден в Marzban")
                return None
            else:
                logger.warning(f"Ошибка API для пользователя {clean_username}: {response.status_code}")
                logger.warning(f"Ответ: {response.text}")
                return None
                
        except Exception as e:
            logger.warning(f"API недоступен для пользователя {clean_username}: {e}")
            return None
    
    def get_user_status(self, user_data: Dict) -> str:
        """Определить статус пользователя"""
        if not user_data:
            return "inactive"
        
        status = user_data.get('status', 'inactive')
        
        if status == 'active':
            # Проверяем срок действия
            expire = user_data.get('expire')
            if expire:
                # Если expire это строка, парсим её
                if isinstance(expire, str):
                    expire_date = datetime.fromisoformat(expire.replace('Z', '+00:00'))
                else:
                    expire_date = datetime.fromtimestamp(expire)
                
                if expire_date < datetime.now():
                    return "expired"
            
            # Проверяем лимит трафика
            data_limit = user_data.get('data_limit')
            used_traffic = user_data.get('used_traffic', 0)
            if data_limit and used_traffic >= data_limit:
                return "limited"
        
        return status
    
    def get_days_remaining(self, user_data: Dict) -> int:
        """Получить количество дней до истечения"""
        if not user_data:
            return 0
        
        expire = user_data.get('expire')
        if not expire:
            return 999  # Безлимитная подписка
        
        # Если expire это строка, парсим её
        if isinstance(expire, str):
            expire_date = datetime.fromisoformat(expire.replace('Z', '+00:00'))
        else:
            expire_date = datetime.fromtimestamp(expire)
        
        now = datetime.now()
        
        if expire_date < now:
            return 0
        
        return (expire_date - now).days
    
    def get_traffic_usage(self, user_data: Dict) -> Dict:
        """Получить информацию об использовании трафика"""
        if not user_data:
            return {"used": 0, "limit": "∞", "percent": 0}
        
        used = user_data.get('used_traffic', 0) or 0
        limit = user_data.get('data_limit', 0) or 0
        
        # Всегда показываем бесконечный трафик
        return {
            "used": used,
            "limit": "∞",
            "percent": 0
        }
    
    def format_traffic(self, bytes_value: int) -> str:
        """Форматировать трафик в читаемый вид"""
        if bytes_value == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = bytes_value
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.1f} {units[unit_index]}"
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Получить полную информацию о пользователе"""
        user_data = self.get_user_by_username(username)
        if not user_data:
            return None
        
        # Извлекаем ссылки из user_data
        links = user_data.get('links', [])
        subscription_url = user_data.get('subscription_url', '')
        
        status = self.get_user_status(user_data)
        days_remaining = self.get_days_remaining(user_data)
        traffic = self.get_traffic_usage(user_data)
        
        return {
            "username": username,
            "status": status,
            "days_remaining": days_remaining,
            "traffic": traffic,
            "subscription_url": subscription_url,
            "links": links,
            "user_data": user_data
        }
    
    def create_test_user(self, username: str, telegram_id: int) -> Optional[Dict]:
        """Создать пользователя с тестовым периодом на 7 дней"""
        import uuid
        
        clean_username = username.lstrip('@')
        
        # Вычисляем дату окончания тестового периода (7 дней)
        expire_date = datetime.now() + timedelta(days=7)
        expire_timestamp = int(expire_date.timestamp())
        
        # Генерируем UUID для пользователя
        user_uuid = str(uuid.uuid4())
        
        # Минимальная структура для создания пользователя
        user_data = {
            "username": clean_username,
            "expire": expire_timestamp,
            "data_limit": 0,  # Бесконечный трафик
            "status": "active",
            "proxies": {
                "vless": {
                    "id": user_uuid,
                    "flow": "xtls-rprx-vision"
                }
            }
        }
        
        try:
            logger.info(f"Отправляем данные для создания пользователя {clean_username}: {json.dumps(user_data, indent=2)}")
            
            response = self.session.post(
                f"{self.api_url}/user",
                json=user_data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"Создан тестовый пользователь {clean_username}")
                return response.json()
            else:
                logger.warning(f"Ошибка создания пользователя {clean_username}: {response.status_code}")
                logger.warning(f"Ответ API: {response.text}")
                return None
                
        except Exception as e:
            logger.warning(f"API недоступен для создания пользователя {clean_username}: {e}")
            return None
