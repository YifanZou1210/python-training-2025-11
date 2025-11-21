from flask import Flask, jsonify
from models import db
from customer_service import customers_bp
from order_service import orders_bp
from auth_service import auth_bp  # New!

app = Flask(__name__)
app.config.from_object('db_config')
db.init_app(app)

app.register_blueprint(auth_bp)       
app.register_blueprint(customers_bp)  
app.register_blueprint(orders_bp)     


@app.route('/')
def home():
    """API documentation"""
    return jsonify({
        'message': 'Customer & Orders API with RBAC',
        'authentication': {
            'POST /api/login': 'Login and get JWT token',
            'POST /api/register': 'Register new user (Admin only)'
        },
        'customers': {
            'GET /api/customers': 'Get all (requires: view_customers)',
            'POST /api/customers': 'Create (requires: create_customers)',
            'PUT /api/customers/<id>': 'Update (requires: update_customers)',
            'DELETE /api/customers/<id>': 'Delete (requires: delete_customers)'
        },
        'orders': {
            'GET /api/orders': 'Get all (requires: view_orders)',
            'POST /api/orders': 'Create (requires: create_orders)',
            'PUT /api/orders/<id>': 'Update (requires: update_orders)',
            'DELETE /api/orders/<id>': 'Delete (requires: delete_orders)'
        }
    }), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, port=5000)