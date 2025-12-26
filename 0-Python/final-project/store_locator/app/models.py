"""
数据库模型定义
包含所有表结构和业务逻辑
"""
from datetime import datetime
from store_locator.app.extensions import db
import bcrypt
import hashlib

store_services = db.Table('store_services',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)

role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

# 店铺模型

class Store(db.Model):
    """
    店铺模型
    
    关键字段:
    - store_id: 业务主键（如S0001）
    - latitude/longitude: 地理坐标（用于距离计算）
    - status: 状态（active/inactive/temporarily_closed）
    - services: 多对多关系，店铺提供的服务
    """
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    store_type = db.Column(db.String(20), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default='active', index=True)
    
    # 地理坐标（复合索引）
    latitude = db.Column(db.Numeric(10, 7), nullable=False)
    longitude = db.Column(db.Numeric(10, 7), nullable=False)
    
    # 地址信息
    address_street = db.Column(db.String(255), nullable=False)
    address_city = db.Column(db.String(100), nullable=False)
    address_state = db.Column(db.String(2), nullable=False)
    address_postal_code = db.Column(db.String(10), nullable=False, index=True)
    address_country = db.Column(db.String(3), nullable=False, default='USA')
    phone = db.Column(db.String(20))
    
    # 营业时间
    hours_mon = db.Column(db.String(20))
    hours_tue = db.Column(db.String(20))
    hours_wed = db.Column(db.String(20))
    hours_thu = db.Column(db.String(20))
    hours_fri = db.Column(db.String(20))
    hours_sat = db.Column(db.String(20))
    hours_sun = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    services = db.relationship('Service', secondary=store_services, backref='stores')
    
    # 复合索引
    __table_args__ = (
        db.Index('idx_store_coordinates', 'latitude', 'longitude'),
    )
    
    def to_dict(self, include_distance=False, distance=None):
        """转换为字典格式"""
        return {
            'id': self.store_id,
            'name': self.name,
            'type': self.store_type,
            'status': self.status,
            'address': {
                'street': self.address_street,
                'city': self.address_city,
                'state': self.address_state,
                'postal_code': self.address_postal_code,
                'country': self.address_country
            },
            'phone': self.phone,
            'coordinates': {
                'latitude': float(self.latitude),
                'longitude': float(self.longitude)
            },
            'services': [s.name for s in self.services],
            'hours': {
                'monday': self.hours_mon,
                'tuesday': self.hours_tue,
                'wednesday': self.hours_wed,
                'thursday': self.hours_thu,
                'friday': self.hours_fri,
                'saturday': self.hours_sat,
                'sunday': self.hours_sun
            },
            'distance_miles': round(distance, 2) if include_distance and distance else None,
            'is_open_now': self.is_open_now()
        }
    
    def is_open_now(self):
        """判断店铺当前是否营业"""
        if self.status != 'active':
            return False
        
        now = datetime.utcnow()
        weekday = now.weekday()
        hours_map = [self.hours_mon, self.hours_tue, self.hours_wed,
                     self.hours_thu, self.hours_fri, self.hours_sat, self.hours_sun]
        today_hours = hours_map[weekday]
        
        if not today_hours or today_hours.lower() == 'closed':
            return False
        
        try:
            open_time, close_time = today_hours.split('-')
            oh, om = map(int, open_time.split(':'))
            ch, cm = map(int, close_time.split(':'))
            current = now.hour * 60 + now.minute
            return (oh * 60 + om) <= current <= (ch * 60 + cm)
        except:
            return False

# ============================================================
# 服务模型
# ============================================================

class Service(db.Model):
    """店铺服务"""
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)

# ============================================================
# 用户模型
# ============================================================

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='active')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='users')
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def has_permission(self, perm):
        """检查权限"""
        return any(p.name == perm for p in self.role.permissions)

# ============================================================
# 角色和权限模型
# ============================================================

class Role(db.Model):
    """角色模型"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary=role_permissions, backref='roles')

class Permission(db.Model):
    """权限模型"""
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# ============================================================
# Refresh Token模型
# ============================================================

class RefreshToken(db.Model):
    """Refresh Token存储"""
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    token_hash = db.Column(db.String(255), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def hash_token(token):
        """对token进行SHA256哈希"""
        return hashlib.sha256(token.encode()).hexdigest()