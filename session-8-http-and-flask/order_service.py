"""
Order API Service
RESTful endpoints for Order operations
"""

from flask import Blueprint, jsonify, request # type: ignore[import]
from models import db, Order, Customer
from datetime import datetime

# Create Blueprint
orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


 
# GET /api/orders - Get all orders
 

@orders_bp.route('/', methods=['GET'])
def get_all_orders():
    """
    Get all orders
    
    Returns:
    - 200: List of orders
    """
    # Query all orders
    orders = db.session.execute(db.select(Order)).scalars().all()
    
    # Convert to dictionary list
    result = [
        {
            'id': o.id,
            'customer_id': o.customer_id,
            'order_date': o.order_date.isoformat() if o.order_date else None,
            'total_amount': float(o.total_amount) if o.total_amount else 0,
            'status': o.status,
            'customer_name': o.customer.name if o.customer else None
        }
        for o in orders
    ]
    
    return jsonify(result), 200


 
# GET /api/orders/<id> - Get single order
 

@orders_bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    """
    Get single order (including customer info)
    
    Returns:
    - 200: Order information
    - 404: Order not found
    """
    # Query order
    order = db.session.execute(
        db.select(Order).where(Order.id == id)
    ).scalar()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Build response
    result = {
        'id': order.id,
        'customer_id': order.customer_id,
        'order_date': order.order_date.isoformat() if order.order_date else None,
        'total_amount': float(order.total_amount) if order.total_amount else 0,
        'status': order.status,
        'customer': {
            'id': order.customer.id,
            'name': order.customer.name,
            'email': order.customer.email
        } if order.customer else None
    }
    
    return jsonify(result), 200


 
# POST /api/orders - Create order
 

@orders_bp.route('/', methods=['POST'])
def create_order():
    """
    Create new order
    
    Request body:
    {
        "customer_id": 1,
        "total_amount": 99.99,
        "status": "pending"  # Optional, defaults to 'pending'
    }
    
    Returns:
    - 201: Created successfully
    - 400: Missing required fields or customer not found
    - 500: Server error
    """
    data = request.get_json()
    
    # Validate required fields
    if not data or 'customer_id' not in data or 'total_amount' not in data:
        return jsonify({'error': 'customer_id and total_amount are required'}), 400
    
    try:
        # Verify customer exists
        customer = db.session.execute(
            db.select(Customer).where(Customer.id == data['customer_id'])
        ).scalar()
        
        if not customer:
            return jsonify({'error': f"Customer {data['customer_id']} not found"}), 400
        
        # Create order
        order = Order(
            customer_id=data['customer_id'],
            total_amount=data['total_amount'],
            status=data.get('status', 'pending')  # Default to 'pending'
        )
        
        # Save to database
        db.session.add(order)
        db.session.commit()
        
        # Return created order
        return jsonify({
            'id': order.id,
            'customer_id': order.customer_id,
            'order_date': order.order_date.isoformat(),
            'total_amount': float(order.total_amount),
            'status': order.status
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


 
# PUT /api/orders/<id> - Update order
 

@orders_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    """
    Update order
    
    Request body:
    {
        "total_amount": 150.00,  # Optional
        "status": "completed"    # Optional
    }
    
    Returns:
    - 200: Updated successfully
    - 404: Order not found
    - 400: No update data
    - 500: Server error
    """
    # Find order
    order = db.session.execute(
        db.select(Order).where(Order.id == id)
    ).scalar()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Get update data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No update data provided'}), 400
    
    try:
        # Update fields
        if 'total_amount' in data:
            order.total_amount = data['total_amount']
        if 'status' in data:
            order.status = data['status']
        
        # Commit changes
        db.session.commit()
        
        # Return updated order
        return jsonify({
            'id': order.id,
            'customer_id': order.customer_id,
            'order_date': order.order_date.isoformat(),
            'total_amount': float(order.total_amount),
            'status': order.status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


 
# DELETE /api/orders/<id> - Delete order
 

@orders_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    """
    Delete order
    
    Returns:
    - 200: Deleted successfully
    - 404: Order not found
    - 500: Server error
    """
    # Find order
    order = db.session.execute(
        db.select(Order).where(Order.id == id)
    ).scalar()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    try:
        # Delete order
        db.session.delete(order)
        db.session.commit()
        
        return jsonify({'message': f'Order {id} deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500