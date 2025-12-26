"""
管理员路由
处理店铺CRUD和用户管理
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from store_locator.app.auth.decorators import permission_required
from store_locator.app.models import Store, Service, User, Role
from store_locator.app.extensions import db
from store_locator.app.stores.import_csv import import_stores_from_csv

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# ============================================================
# 店铺管理端点
# ============================================================

@admin_bp.route('/stores', methods=['GET'])
@permission_required('view_stores')
def list_stores(current_user):
    """
    获取店铺列表（带分页）
    
    查询参数:
        page: 页码（默认1）
        per_page: 每页数量（默认20）
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Store.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'stores': [s.to_dict() for s in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': pagination.pages,
            'total_items': pagination.total
        }
    }), 200

@admin_bp.route('/stores', methods=['POST'])
@permission_required('manage_stores')
def create_store(current_user):
    """
    创建新店铺
    
    请求体:
    {
        "store_id": "S9999",
        "name": "Test Store",
        "store_type": "regular",
        "latitude": 42.36,
        "longitude": -71.06,
        "address_street": "123 Test St",
        "address_city": "Boston",
        "address_state": "MA",
        "address_postal_code": "02101",
        "phone": "617-555-0000",
        "services": ["pharmacy", "pickup"]
    }
    """
    data = request.get_json()
    
    # 验证必填字段
    required = ['store_id', 'name', 'store_type', 'address_street',
                'address_city', 'address_state', 'address_postal_code']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # 检查store_id是否已存在
    if Store.query.filter_by(store_id=data['store_id']).first():
        return jsonify({'error': 'Store ID already exists'}), 400
    
    # 创建店铺
    store = Store(
        store_id=data['store_id'],
        name=data['name'],
        store_type=data['store_type'],
        status=data.get('status', 'active'),
        latitude=data.get('latitude', 0),
        longitude=data.get('longitude', 0),
        address_street=data['address_street'],
        address_city=data['address_city'],
        address_state=data['address_state'],
        address_postal_code=data['address_postal_code'],
        address_country=data.get('address_country', 'USA'),
        phone=data.get('phone'),
        hours_mon=data.get('hours_mon'),
        hours_tue=data.get('hours_tue'),
        hours_wed=data.get('hours_wed'),
        hours_thu=data.get('hours_thu'),
        hours_fri=data.get('hours_fri'),
        hours_sat=data.get('hours_sat'),
        hours_sun=data.get('hours_sun')
    )
    
    # 添加服务
    if 'services' in data and data['services']:
        for svc_name in data['services']:
            svc = Service.query.filter_by(name=svc_name).first()
            if svc:
                store.services.append(svc)
    
    db.session.add(store)
    db.session.commit()
    
    return jsonify(store.to_dict()), 201

@admin_bp.route('/stores/<store_id>', methods=['GET'])
@permission_required('view_stores')
def get_store(current_user, store_id):
    """获取单个店铺详情"""
    store = Store.query.filter_by(store_id=store_id).first()
    if not store:
        return jsonify({'error': 'Store not found'}), 404
    
    return jsonify(store.to_dict()), 200

@admin_bp.route('/stores/<store_id>', methods=['PATCH'])
@permission_required('manage_stores')
def update_store(current_user, store_id):
    """
    部分更新店铺
    
    只允许更新以下字段:
    - name, phone, status
    - hours_mon ~ hours_sun
    - services
    """
    store = Store.query.filter_by(store_id=store_id).first()
    if not store:
        return jsonify({'error': 'Store not found'}), 404
    
    data = request.get_json()
    
    # 允许更新的字段
    allowed_fields = ['name', 'phone', 'status', 'hours_mon', 'hours_tue',
                      'hours_wed', 'hours_thu', 'hours_fri', 'hours_sat', 'hours_sun']
    
    # 更新字段
    for field in allowed_fields:
        if field in data:
            setattr(store, field, data[field])
    
    # 更新服务（特殊处理）
    if 'services' in data:
        store.services = []
        for svc_name in data['services']:
            svc = Service.query.filter_by(name=svc_name).first()
            if svc:
                store.services.append(svc)
    
    store.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(store.to_dict()), 200

@admin_bp.route('/stores/<store_id>', methods=['DELETE'])
@permission_required('manage_stores')
def delete_store(current_user, store_id):
    """
    软删除店铺
    
    注意: 不物理删除，只设置status='inactive'
    """
    store = Store.query.filter_by(store_id=store_id).first()
    if not store:
        return jsonify({'error': 'Store not found'}), 404
    
    store.status = 'inactive'
    db.session.commit()
    
    return jsonify({'message': 'Store deactivated successfully'}), 200

# ============================================================
# CSV导入端点
# ============================================================

@admin_bp.route('/stores/import', methods=['POST'])
@permission_required('import_data')
def import_csv(current_user):
    """
    批量导入店铺CSV
    
    请求:
    - Content-Type: multipart/form-data
    - file: CSV文件
    
    返回:
    {
        "success": true,
        "total_rows": 50,
        "created": 30,
        "updated": 20
    }
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be CSV format'}), 400
    
    result = import_stores_from_csv(file)
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result), 200

# ============================================================
# 用户管理端点（Admin Only）
# ============================================================

@admin_bp.route('/users', methods=['GET'])
@permission_required('manage_users')
def list_users(current_user):
    """获取用户列表"""
    users = User.query.all()
    return jsonify({
        'users': [{
            'id': u.id,
            'email': u.email,
            'role': u.role.name,
            'status': u.status,
            'created_at': u.created_at.isoformat()
        } for u in users]
    }), 200

@admin_bp.route('/users', methods=['POST'])
@permission_required('manage_users')
def create_user(current_user):
    """创建新用户"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password') or not data.get('role'):
        return jsonify({'error': 'Email, password and role required'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    role = Role.query.filter_by(name=data['role']).first()
    if not role:
        return jsonify({'error': 'Invalid role'}), 400
    
    user = User(email=data['email'], role=role)
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'role': user.role.name
    }), 201