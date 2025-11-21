from flask import Flask, Blueprint, jsonify, request  # type: ignore[import]
from models import db, Customer, CustomerProfile

customers_bp = Blueprint('customers', __name__, url_prefix = 'api/customers')

# get /api/customer 

@customers_bp.route('/', methods = ['GET'])
def get_all_customers():
    customers = db.session.execute(db.select(Customer)).scalars().all()
    result = [
        {
            'id': c.id,
            'name':c.name, 
            'email':c.email,
            'created_at': c.created_at.isoformat() if c.created_at else None 
        }
        for c in customers 
    ]
    return jsonify(result), 200

@customers_bp.route('/<int:id>', methods=['GET'])
def get_customer(id):
    customer = db.session.execute(db.select(Customer).where(Customer.id == id)).scalar()
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    result = {
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'created_at': customer.created_at.isoformat() if customer.created_at else None,
        'profile': None
    }
    
    if customer.profile:
        result['profile'] = {
            'phone': customer.profile.phone,
            'address': customer.profile.address,
            'date_of_birth': customer.profile.date_of_birth.isoformat() if customer.profile.date_of_birth else None
        }
    
    return jsonify(result), 200

@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email are required'}), 404
    try:
        customer = Customer(
            name=data['name'],
            email=data['email']
        )
        
        # 如果有 profile 数据，创建 profile
        if 'profile' in data and data['profile']:
            profile_data = data['profile']
            profile = CustomerProfile(
                phone=profile_data.get('phone'),
                address=profile_data.get('address'),
                date_of_birth=profile_data.get('date_of_birth')
            )
            customer.profile = profile
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'created_at': customer.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = db.session.execute(
        db.select(Customer).where(Customer.id == id)
    ).scalar()
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No update data provided'}), 400
    
    try:
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
    
        db.session.commit()
        
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'created_at': customer.created_at.isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """
    delete customer 
    
    返回：
    - 200: success
    - 404: not exist 
    - 500: server error 
    """
    customer = db.session.execute(
        db.select(Customer).where(Customer.id == id)
    ).scalar()
    
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    try:
        # 删除客户（CASCADE 会删除 profile 和 orders）
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({'message': f'Customer {id} deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500