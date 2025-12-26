"""
认证路由
处理登录、刷新、登出
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from store_locator.app.models import User, RefreshToken
from store_locator.app.extensions import db
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    
    请求体:
    {
        "email": "admin@test.com",
        "password": "AdminTest123!"
    }
    
    返回:
    {
        "access_token": "...",
        "refresh_token": "...",
        "user": {"email": "...", "role": "admin"}
    }
    """
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    email = data['email'].strip().lower() 
    password = data['password']

    # 查找用户
    user = User.query.filter_by(email=email).first()
    print("Password hash in DB:", user.password_hash)
    print("Check password result:", user.check_password(password))

    
    # 验证密码
    if not user or not user.check_password(data['password']):
        print("Trying login for:", email, password)
        return jsonify({'error': 'Invalid email or password'}), 401
    if not user:
        print("User not found")
    else:
        print("User found. Password check:", user.check_password(data['password']))
        print("User status:", user.status)

    # 检查用户状态
    if user.status != 'active':
        return jsonify({'error': 'Account is inactive'}), 403

    # 生成tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    # 存储refresh token到数据库
    token_hash = RefreshToken.hash_token(refresh_token)
    rt = RefreshToken(
        token_hash=token_hash,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.session.add(rt)
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role.name
        }
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    刷新access token
    
    请求头:
    Authorization: Bearer <refresh_token>
    
    返回:
    {
        "access_token": "..."
    }
    """
    user_id = int(get_jwt_identity())
    
    # 验证用户
    user = User.query.get(user_id)
    if not user or user.status != 'active':
        return jsonify({'error': 'Invalid user'}), 401
    
    # 生成新的access token
    new_access_token = create_access_token(identity=str(user_id))
    
    return jsonify({'access_token': new_access_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    """
    登出（撤销refresh token）
    
    请求头:
    Authorization: Bearer <refresh_token>
    """
    user_id = int(get_jwt_identity())
    
    # 删除该用户的所有refresh tokens
    RefreshToken.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    return jsonify({'message': 'Successfully logged out'}), 200