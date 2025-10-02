#!/usr/bin/env python3
"""
API для работы с Marzban
"""

import requests
import os
from urllib.parse import quote
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
        links = user_data.get('links', []) or []
        subscription_url = user_data.get('subscription_url', '')
        if not subscription_url:
            # Доп. фолбэк: шаблон из переменной окружения, например: https://panel.example.com/sub/{username}
            tmpl = os.environ.get('SUBSCRIPTION_FALLBACK_TEMPLATE')
            if tmpl and '{username}' in tmpl:
                subscription_url = tmpl.replace('{username}', username.lstrip('@'))

        # Fallback: если панель не выдает ссылки, пробуем собрать VLESS Reality вручную из env
        try:
            if not links and user_data.get('proxies', {}).get('vless', {}).get('id'):
                uuid = user_data['proxies']['vless']['id']
                host = os.environ.get('VLESS_HOST') or os.environ.get('SERVER_HOST') or os.environ.get('DOMAIN')
                port = os.environ.get('VLESS_PORT') or os.environ.get('PORT') or '443'
                pbk = os.environ.get('REALITY_PBK')
                sni = os.environ.get('REALITY_SNI') or host
                short_id = os.environ.get('REALITY_SHORT_ID') or os.environ.get('REALITY_SID')
                fp = os.environ.get('VLESS_FP', 'chrome')
                alpn = os.environ.get('VLESS_ALPN', 'h2')
                label = os.environ.get('VLESS_LABEL', 'YoVPN')
                if host and pbk:
                    query = [
                        'type=tcp',
                        'security=reality',
                        f'pbk={pbk}',
                        'flow=xtls-rprx-vision'
                    ]
                    if sni:
                        query.append(f'sni={sni}')
                    if fp:
                        query.append(f'fp={fp}')
                    if alpn:
                        query.append(f'alpn={alpn}')
                    if short_id:
                        query.append(f'sid={short_id}')
                    q = '&'.join(query)
                    link = f"vless://{uuid}@{host}:{port}?{q}#{quote(label)}"
                    links = [link]
        except Exception:
            pass
        
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

    def set_user_inbounds(self, username: str, inbounds_map: Dict[str, list]) -> bool:
        """Назначить пользователю теги инбаундов по протоколам, например {"vless": ["VLESS TCP REALITY"]}."""
        try:
            payload = {"inbounds": inbounds_map}
            resp = self.session.patch(f"{self.api_url}/user/{username}", json=payload, timeout=self.timeout)
            if resp.status_code in (200, 204):
                logger.info(f"Назначены inbounds {inbounds_map} пользователю {username}")
                return True
            logger.warning(f"Не удалось назначить inbounds {inbounds_map} для {username}: {resp.status_code} {resp.text}")
            return False
        except Exception as e:
            logger.error(f"set_user_inbounds error: {e}")
            return False

    # ===== Баланс → дни → продление подписки =====
    def extend_user_by_days(self, username: str, add_days: int) -> bool:
        """Продлевает срок действия пользователя на add_days от текущей даты (или от текущего expire)."""
        try:
            user = self.get_user_by_username(username)
            if not user:
                return False
            now = datetime.now()
            expire = user.get('expire')
            if isinstance(expire, str):
                base = datetime.fromisoformat(expire.replace('Z', '+00:00'))
            elif expire:
                base = datetime.fromtimestamp(expire)
            else:
                base = now
            if base < now:
                base = now
            new_expire = base + timedelta(days=add_days)
            payload = {"expire": int(new_expire.timestamp())}
            resp = self.session.patch(f"{self.api_url}/user/{username}", json=payload, timeout=self.timeout)
            if resp.status_code in (200, 204):
                logger.info(f"Продлен пользователь {username} на {add_days} дней (до {new_expire})")
                return True
            logger.warning(f"Не удалось продлить {username}: {resp.status_code} {resp.text}")
            return False
        except Exception as e:
            logger.error(f"extend_user_by_days error: {e}")
            return False

    def apply_balance_as_days(self, username: str, balance_rub: int) -> bool:
        """Устанавливает expire как now + (balance_rub // 4) дней (абсолютно), не наращивая при каждом вызове."""
        try:
            user = self.get_user_by_username(username)
            if not user:
                return False
            days = max(0, balance_rub // 4)
            target = datetime.now() + timedelta(days=days)
            ts = int(target.timestamp())
            payload = {"expire": ts}
            # Сначала пробуем PATCH
            resp = self.session.patch(f"{self.api_url}/user/{username}", json=payload, timeout=self.timeout)
            if resp.status_code in (200, 204):
                logger.info(f"Установлен expire {username} = now+{days} дней ({target}) [PATCH]")
                return True
            # Если метод не разрешен, пробуем PUT
            if resp.status_code == 405:
                resp2 = self.session.put(f"{self.api_url}/user/{username}", json=payload, timeout=self.timeout)
                if resp2.status_code in (200, 204):
                    logger.info(f"Установлен expire {username} = now+{days} дней ({target}) [PUT]")
                    return True
                logger.warning(f"Не удалось установить expire {username} (PUT): {resp2.status_code} {resp2.text}")
                return False
            logger.warning(f"Не удалось установить expire {username}: {resp.status_code} {resp.text}")
            return False
        except Exception as e:
            logger.error(f"apply_balance_as_days error: {e}")
            return False
    
    def create_test_user(self, username: str, telegram_id: int) -> Optional[Dict]:
        """Создать пользователя с тестовым периодом на 7 дней"""
        import uuid
        
        clean_username = username.lstrip('@')
        
        # Вычисляем дату окончания тестового периода (5 дней под приветственный баланс 20 ₽)
        expire_date = datetime.now() + timedelta(days=5)
        expire_timestamp = int(expire_date.timestamp())
        
        # Генерируем UUID для пользователя
        user_uuid = str(uuid.uuid4())
        
        # Минимальная структура для создания пользователя
        inbound_tag = os.environ.get('VLESS_INBOUND_TAG', 'VLESS TCP REALITY')

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
            },
            # Некоторые версии API поддерживают поле inbounds при создании
            "inbounds": {"vless": [inbound_tag]}
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
                created = response.json()
                # Доп. попытка назначить inbound тег патчем, если требуется
                try:
                    self.set_user_inbounds(clean_username, {"vless": [inbound_tag]})
                except Exception:
                    pass
                return created
            else:
                logger.warning(f"Ошибка создания пользователя {clean_username}: {response.status_code}")
                logger.warning(f"Ответ API: {response.text}")
                return None
                
        except Exception as e:
            logger.warning(f"API недоступен для создания пользователя {clean_username}: {e}")
            return None
