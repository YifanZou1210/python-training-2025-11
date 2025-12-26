"""
Flask应用工厂函数
负责创建和配置Flask应用
"""
from flask import Flask
from flask_cors import CORS
from store_locator.app.extensions import db, jwt, migrate, limiter, cache
from store_locator.app.config import Config

def create_app():
    """
    创建Flask应用实例
    
    功能:
    1. 加载配置
    2. 初始化所有扩展（数据库、JWT、缓存等）
    3. 注册所有蓝图（路由模块）
    4. 配置CORS
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)
    
    # CORS配置（允许跨域）
    CORS(app)
    
    # 注册蓝图
    from store_locator.app.auth.routes import auth_bp
    from store_locator.app.stores.routes import stores_bp
    from store_locator.app.admin.routes import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(stores_bp)
    app.register_blueprint(admin_bp)
    
    # 健康检查端点
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app