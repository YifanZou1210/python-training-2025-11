
from flask import Flask
from flask_cors import CORS
from store_locator.app.extensions import db, jwt, migrate, limiter, cache
from store_locator.app.config import Config

def create_app():
    app = Flask(__name__)
    

    app.config.from_object(Config)
    

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)
    

    CORS(app)
    

    from store_locator.app.auth.routes import auth_bp
    from store_locator.app.stores.routes import stores_bp
    from store_locator.app.admin.routes import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(stores_bp)
    app.register_blueprint(admin_bp)
    

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    return app