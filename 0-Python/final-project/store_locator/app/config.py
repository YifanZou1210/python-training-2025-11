"""
应用配置文件
包含所有环境变量和配置参数
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置类"""
    
    # Flask基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)    # Access Token 15分钟
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)       # Refresh Token 7天
    
    # Redis配置
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # 缓存配置
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300  # 5分钟
    
    # 速率限制配置
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_HEADERS_ENABLED = True
    
    # 地理编码配置
    GEOCODING_SERVICE = os.getenv('GEOCODING_SERVICE', 'nominatim')
    NOMINATIM_USER_AGENT = os.getenv('NOMINATIM_USER_AGENT', 'store-locator/1.0')