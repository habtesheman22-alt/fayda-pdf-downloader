#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache Manager for Redis integration
Provides caching for OTP and session data to improve performance
"""

import json
import logging
import hashlib
from typing import Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not installed. Using in-memory cache fallback.")


class InMemoryCache:
    """In-memory cache fallback when Redis is not available"""
    
    def __init__(self):
        """Initialize in-memory cache"""
        self._cache = {}
    
    def set(self, key: str, value: Any, ttl: int = 600) -> bool:
        """Set value in cache with TTL"""
        try:
            self._cache[key] = {
                'value': value,
                'expires_at': datetime.utcnow() + timedelta(seconds=ttl)
            }
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {str(e)}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if key in self._cache:
                entry = self._cache[key]
                if datetime.utcnow() < entry['expires_at']:
                    return entry['value']
                else:
                    del self._cache[key]
            return None
        except Exception as e:
            logger.error(f"Error getting cache: {str(e)}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if key in self._cache:
                del self._cache[key]
            return True
        except Exception as e:
            logger.error(f"Error deleting cache: {str(e)}")
            return False
    
    def flush(self) -> bool:
        """Clear all cache"""
        try:
            self._cache.clear()
            return True
        except Exception as e:
            logger.error(f"Error flushing cache: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        return {
            'size': len(self._cache),
            'type': 'in-memory'
        }


class RedisCache:
    """Redis-based cache for distributed systems"""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: str = None):
        """Initialize Redis connection"""
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True
            )
            # Test connection
            self.client.ping()
            logger.info("Redis connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    def set(self, key: str, value: Any, ttl: int = 600) -> bool:
        """Set value in cache with TTL"""
        try:
            if isinstance(value, dict) or isinstance(value, list):
                value = json.dumps(value)
            
            self.client.setex(key, ttl, str(value))
            logger.debug(f"Cache set: {key}")
            return True
        except Exception as e:
            logger.error(f"Error setting Redis cache: {str(e)}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.client.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            logger.debug(f"Cache miss: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting Redis cache: {str(e)}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting Redis cache: {str(e)}")
            return False
    
    def flush(self) -> bool:
        """Clear all cache"""
        try:
            self.client.flushdb()
            logger.info("Redis cache flushed")
            return True
        except Exception as e:
            logger.error(f"Error flushing Redis cache: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        try:
            info = self.client.info()
            return {
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_commands': info.get('total_commands_processed'),
                'type': 'redis'
            }
        except Exception as e:
            logger.error(f"Error getting Redis stats: {str(e)}")
            return {}


class CacheManager:
    """Unified cache manager interface"""
    
    _instance = None
    
    def __new__(cls, use_redis: bool = False, **redis_config):
        """Singleton pattern for cache manager"""
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance._initialize(use_redis, **redis_config)
        return cls._instance
    
    def _initialize(self, use_redis: bool = False, **redis_config) -> None:
        """Initialize cache backend"""
        try:
            if use_redis and REDIS_AVAILABLE:
                self.cache = RedisCache(**redis_config)
                logger.info("CacheManager initialized with Redis")
            else:
                if use_redis and not REDIS_AVAILABLE:
                    logger.warning("Redis requested but not available, using in-memory cache")
                self.cache = InMemoryCache()
                logger.info("CacheManager initialized with in-memory cache")
        except Exception as e:
            logger.error(f"Error initializing CacheManager: {str(e)}")
            self.cache = InMemoryCache()
    
    def set_otp(self, user_id: int, fan_number: str, otp_data: dict, ttl: int = 600) -> bool:
        """Cache OTP data"""
        key = self._make_otp_key(user_id, fan_number)
        return self.cache.set(key, otp_data, ttl)
    
    def get_otp(self, user_id: int, fan_number: str) -> Optional[dict]:
        """Get cached OTP data"""
        key = self._make_otp_key(user_id, fan_number)
        return self.cache.get(key)
    
    def delete_otp(self, user_id: int, fan_number: str) -> bool:
        """Delete cached OTP data"""
        key = self._make_otp_key(user_id, fan_number)
        return self.cache.delete(key)
    
    def set_session(self, user_id: int, session_data: dict, ttl: int = 86400) -> bool:
        """Cache session data"""
        key = self._make_session_key(user_id)\n        return self.cache.set(key, session_data, ttl)\n    \n    def get_session(self, user_id: int) -> Optional[dict]:\n        \"\"\"Get cached session data\"\"\"\n        key = self._make_session_key(user_id)\n        return self.cache.get(key)\n    \n    def delete_session(self, user_id: int) -> bool:\n        \"\"\"Delete cached session data\"\"\"\n        key = self._make_session_key(user_id)\n        return self.cache.delete(key)\n    \n    def set_user(self, user_id: int, user_data: dict, ttl: int = 3600) -> bool:\n        \"\"\"Cache user data\"\"\"\n        key = self._make_user_key(user_id)\n        return self.cache.set(key, user_data, ttl)\n    \n    def get_user(self, user_id: int) -> Optional[dict]:\n        \"\"\"Get cached user data\"\"\"\n        key = self._make_user_key(user_id)\n        return self.cache.get(key)\n    \n    def delete_user(self, user_id: int) -> bool:\n        \"\"\"Delete cached user data\"\"\"\n        key = self._make_user_key(user_id)\n        return self.cache.delete(key)\n    \n    def invalidate_user_cache(self, user_id: int) -> None:\n        \"\"\"Invalidate all user-related cache\"\"\"\n        self.delete_session(user_id)\n        self.delete_user(user_id)\n        logger.info(f\"User cache invalidated for user {user_id}\")\n    \n    @staticmethod\n    def _make_otp_key(user_id: int, fan_number: str) -> str:\n        \"\"\"Generate OTP cache key\"\"\"\n        return f\"otp:{user_id}:{fan_number}\"\n    \n    @staticmethod\n    def _make_session_key(user_id: int) -> str:\n        \"\"\"Generate session cache key\"\"\"\n        return f\"session:{user_id}\"\n    \n    @staticmethod\n    def _make_user_key(user_id: int) -> str:\n        \"\"\"Generate user cache key\"\"\"\n        return f\"user:{user_id}\"\n    \n    def flush_all(self) -> bool:\n        \"\"\"Clear all cache\"\"\"\n        return self.cache.flush()\n    \n    def get_stats(self) -> dict:\n        \"\"\"Get cache statistics\"\"\"\n        return self.cache.get_stats()\n\n\n# Global cache manager instance\ncache_manager = CacheManager()\n"