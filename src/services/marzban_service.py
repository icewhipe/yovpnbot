#!/usr/bin/env python3
"""
Улучшенный сервис для работы с Marzban API
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from ..config import config

logger = logging.getLogger(__name__)

class MarzbanService:
    """Улучшенный сервис для работы с Marzban API"""
    
    def __init__(self, api_url: str = None, admin_token: str = None, timeout: int = 10):
        self.api_url = (api_url or config.MARZBAN_API_URL).rstrip('/')
        self.admin_token = admin_token or config.MARZBAN_ADMIN_TOKEN
        self.timeout = timeout
        self.session = requests.Session()
        
        # Настройка SSL - ВКЛЮЧАЕМ проверку для безопасности
        self.session.verify = True
        
        # Настройка заголовков
        if self.admin_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.admin_token}',
                'Content-Type': 'application/json',
                'User-Agent': 'YOVPN-Bot/1.0'
            })
        
        # Настройка таймаутов
        self.session.timeout = timeout
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Безопасный запрос к API с обработкой ошибок"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            logger.debug(f"Выполняем запрос: {method} {url}")
            response = self.session.request(method, url, **kwargs)
            
            # Логируем запрос для отладки
            logger.debug(f"{method} {url} - Status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.info(f"Ресурс не найден: {endpoint}")
                return None
            elif response.status_code == 401:
                logger.error(f"Ошибка авторизации в Marzban API. URL: {url}")
                logger.error(f"Токен: {self.admin_token[:10]}..." if self.admin_token else "Токен не установлен")
                logger.error(f"Ответ сервера: {response.text}")
                return None
            elif response.status_code == 403:
                logger.error(f"Доступ запрещен в Marzban API. URL: {url}")
                logger.error(f"Ответ сервера: {response.text}")
                return None
            else:
                logger.warning(f"Ошибка API {endpoint}: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Таймаут запроса к {endpoint}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Ошибка соединения с {endpoint}")
            return None
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL ошибка при запросе к {endpoint}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка запроса к {endpoint}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON ответа от {endpoint}: {e}")
            return None
        except Exception as e:
            logger.error(f"Неожиданная ошибка при запросе к {endpoint}: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Получить пользователя по username"""
        clean_username = username.lstrip('@')
        logger.info(f"Ищем пользователя в Marzban: {clean_username}")
        
        return self._make_request('GET', f'/user/{clean_username}')
    
    def get_user_status(self, user_data: Dict) -> str:
        """Определить статус пользователя"""
        if not user_data:
            return "inactive"
        
        status = user_data.get('status', 'inactive')
        
        if status == 'active':
            # Проверяем срок действия
            expire = user_data.get('expire')
            if expire:
                try:
                    if isinstance(expire, str):
                        expire_date = datetime.fromisoformat(expire.replace('Z', '+00:00'))
                    else:
                        expire_date = datetime.fromtimestamp(expire)
                    
                    if expire_date < datetime.now():
                        return "expired"
                except (ValueError, TypeError) as e:
                    logger.warning(f"Ошибка парсинга даты истечения: {e}")
            
            # Проверяем лимит трафика
            data_limit = user_data.get('data_limit')
            used_traffic = user_data.get('used_traffic', 0)
            if data_limit and data_limit > 0 and used_traffic >= data_limit:
                return "limited"
        
        return status
    
    def get_days_remaining(self, user_data: Dict) -> int:
        """Получить количество дней до истечения"""
        if not user_data:
            return 0
        
        expire = user_data.get('expire')
        if not expire:
            return 999  # Безлимитная подписка
        
        try:
            if isinstance(expire, str):
                expire_date = datetime.fromisoformat(expire.replace('Z', '+00:00'))
            else:
                expire_date = datetime.fromtimestamp(expire)
            
            now = datetime.now()
            
            if expire_date < now:
                return 0
            
            return (expire_date - now).days
        except (ValueError, TypeError) as e:
            logger.warning(f"Ошибка вычисления дней до истечения: {e}")
            return 0
    
    def get_traffic_usage(self, user_data: Dict) -> Dict:
        """Получить информацию об использовании трафика"""
        if not user_data:
            return {"used": 0, "limit": "∞", "percent": 0}
        
        used = user_data.get('used_traffic', 0) or 0
        limit = user_data.get('data_limit', 0) or 0
        
        # Всегда показываем бесконечный трафик для тестовых аккаунтов
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
    
    def create_user(self, username: str, telegram_id: int, days: int = 7, 
                   data_limit: int = 0, proxies: Dict = None) -> Optional[Dict]:
        """Создать пользователя с настраиваемыми параметрами"""
        import uuid
        
        clean_username = username.lstrip('@')
        
        # Вычисляем дату окончания
        expire_date = datetime.now() + timedelta(days=days)
        expire_timestamp = int(expire_date.timestamp())
        
        # Генерируем UUID для пользователя
        user_uuid = str(uuid.uuid4())
        
        # Настройки прокси по умолчанию
        if proxies is None:
            proxies = {
                "vless": {
                    "id": user_uuid,
                    "flow": "xtls-rprx-vision"
                }
            }
        
        # Структура для создания пользователя
        user_data = {
            "username": clean_username,
            "expire": expire_timestamp,
            "data_limit": data_limit,  # 0 = бесконечный трафик
            "status": "active",
            "proxies": proxies
        }
        
        logger.info(f"Создаем пользователя {clean_username} на {days} дней")
        
        return self._make_request('POST', '/user', json=user_data)
    
    def create_test_user(self, username: str, telegram_id: int) -> Optional[Dict]:
        """Создать пользователя с тестовым периодом на 7 дней"""
        return self.create_user(username, telegram_id, days=7, data_limit=0)
    
    def update_user(self, username: str, updates: Dict) -> Optional[Dict]:
        """Обновить данные пользователя"""
        clean_username = username.lstrip('@')
        
        logger.info(f"Обновляем пользователя {clean_username}")
        
        return self._make_request('PUT', f'/user/{clean_username}', json=updates)
    
    def delete_user(self, username: str) -> bool:
        """Удалить пользователя"""
        clean_username = username.lstrip('@')
        
        logger.info(f"Удаляем пользователя {clean_username}")
        
        result = self._make_request('DELETE', f'/user/{clean_username}')
        return result is not None
    
    def get_all_users(self) -> List[Dict]:
        """Получить всех пользователей"""
        result = self._make_request('GET', '/users')
        if result and isinstance(result, list):
            return result
        return []
    
    def health_check(self) -> bool:
        """Проверка доступности API"""
        try:
            logger.info(f"Проверяем доступность Marzban API: {self.api_url}")
            logger.info(f"Используем токен: {self.admin_token[:10]}..." if self.admin_token else "Токен не установлен")
            
            result = self._make_request('GET', '/system')
            if result:
                logger.info("Marzban API доступен")
                return True
            else:
                logger.warning("Marzban API недоступен")
                return False
        except Exception as e:
            logger.error(f"Ошибка проверки здоровья API: {e}")
            return False