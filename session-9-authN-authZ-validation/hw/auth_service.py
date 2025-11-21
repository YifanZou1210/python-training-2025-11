from flask import Blueprint, jsonify, request
from models import db
from model_rbac import User, Role
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

# blueprint name = Blueprint(bp name, __name__, uniform prefix) 
# used as submodule encapsulation 
auth_bp = Blueprint('auth', __name__, url_prefix='/api')

JWT_SECRET = 'jwt'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request body:
    {
        "email": "admin@example.com",
        "password": "Admin123"
    }
    
    Returns:
    - 200: Login successful, returns JWT token
    - 400: Missing fields
    - 401: Invalid credentials
    """
    data = request.get_json()
    # {"email": "admin@example.com","password": "Admin123"}
    # Validate input
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    # jsonify -> (response, status_code)
    
    # Find user by email
    user = db.session.execute(
        db.select(User).where(User.email == data['email'])
    ).scalar()
    
    # Verify user exists and password is correct
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Check if account is active
    if not user.is_active:
        return jsonify({'error': 'Account is inactive'}), 401
    
    # Generate JWT token
    token_payload = {
        'user_id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role.name,
        'permissions': user.get_permissions(),  # Include full permission list
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    
    token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    # Return token and user info
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role.name,
            'permissions': user.get_permissions()
        }
    }), 200



# POST /api/register - Register New User


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user (Admin only!)
    
    This endpoint is protected by @permission_required('manage_users')
    Only users with 'manage_users' permission (Admin) can create new users
    
    Request body:
    {
        "email": "newuser@example.com",
        "password": "Password123",
        "name": "New User",
        "role_id": 2  # Admin assigns role (1=Admin, 2=Sales, 3=Viewer)
    }
    
    Returns:
    - 201: User created successfully
    - 400: Missing fields or invalid role
    - 401: Not authenticated
    - 403: No permission (not admin)
    - 500: Server error
    """
    # This will be protected by @permission_required('manage_users') decorator
    # For now, we implement the logic
    
    data = request.get_json()
    
    # Validate required fields
    if not data or not all(k in data for k in ['email', 'password', 'name', 'role_id']):
        return jsonify({'error': 'email, password, name, and role_id are required'}), 400
    
    try:
        # Verify role exists
        role = db.session.get(Role, data['role_id'])
        if not role:
            return jsonify({'error': f"Role {data['role_id']} not found"}), 400
        
        # Check if email already exists
        existing = db.session.execute(
            db.select(User).where(User.email == data['email'])
        ).scalar()
        
        if existing:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Hash password
        password_hash = generate_password_hash(data['password'])
        
        # Create user
        user = User(
            email=data['email'],
            password_hash=password_hash,
            name=data['name'],
            role_id=data['role_id']
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Return created user (without password hash!)
        return jsonify({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role.name,
            'permissions': user.get_permissions()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



# Authorization Decorator


def permission_required(permission_name):
    """
    Decorator to protect endpoints with permission check
    
    Usage:
        @permission_required('view_customers')
        def get_customers():
            ...
    
    Process:
    1. Extract JWT token from Authorization header
    2. Decode token
    3. Check if required permission is in user's permissions
    4. Allow/deny access
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get Authorization header
            auth_header = request.headers.get('Authorization')
            
            # Check if token exists
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'No token provided'}), 401
            
            # Extract token (format: "Bearer <token>")
            token = auth_header.split(' ')[1]
            
            try:
                # Decode JWT token
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                
                # Extract permissions from token
                user_permissions = payload.get('permissions', [])
                
                # Check if user has required permission
                if permission_name not in user_permissions:
                    return jsonify({
                        'error': f'Permission denied. Required: {permission_name}'
                    }), 403
                
                # Add user info to request context (optional, for logging)
                request.current_user = payload
                
                # Permission granted, proceed with original function
                return func(*args, **kwargs)
                
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
        
        return wrapper
    return decorator



# Helper: Get Current User from Token


def get_current_user():
    """
    Extract current user info from JWT token
    
    Returns: dict with user_id, email, role, permissions
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except:
        return None
