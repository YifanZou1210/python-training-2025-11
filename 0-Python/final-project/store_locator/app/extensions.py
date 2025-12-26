"""
Flask扩展初始化
集中管理所有扩展实例
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# 数据库ORM
db = SQLAlchemy()

# JWT认证
jwt = JWTManager()

# 数据库迁移
migrate = Migrate()

# 速率限制器
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

# 缓存
cache = Cache()