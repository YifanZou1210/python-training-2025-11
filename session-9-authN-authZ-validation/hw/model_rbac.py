from typing import List
from datetime import datetime 
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, Table, Column 
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from models import db, Base 
# Injection table本身没有额外business逻辑，不需要被查询或者操作，不需要创建orm类
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('id',Integer, primary_key = True, autoincrement = True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete = 'CASCADE')),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete = 'CASCADE')),
    Column('created_at', DateTime, default = datetime.now)
)

class Permission(Base):
    __tablename__ = 'permissions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # Many-to-many back-populates relationship with roles
    # Permission中有roles属性，指向Role类中的属性permissions,保证cascade
    roles: Mapped[List["Role"]] = relationship(
        secondary=role_permissions,
        back_populates="permissions"
    )
    
    def __repr__(self):
        return f"<Permission(name='{self.name}')>"

class Role(Base):
    __tablename__ = 'roles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # One-to-many: a role has many users
    # Mapped[List[py-type/class name]] 注意
    users: Mapped[List["User"]] = relationship(
        back_populates="role", # 指向对方类中的attri name 
        cascade="all, delete-orphan"
    )
    
    # Many-to-many: a role has many permissions
    permissions: Mapped[List["Permission"]] = relationship(
        secondary=role_permissions,# 告诉sqlalchemy这个表用作mtm连接table
        back_populates="roles"
    )
    
    def get_permission_names(self):
        """Get list of permission names for this role"""
        return [p.name for p in self.permissions]
    
    def __repr__(self):
        return f"<Role(name='{self.name}')>"
    
class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Foreign key: user belongs to one role
    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id'),
        nullable=False
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    # Many-to-one: many users can have the same role
    role: Mapped["Role"] = relationship(back_populates="users")
    
    def get_permissions(self):
        """Get list of permission names for this user (through role)"""
        return self.role.get_permission_names() if self.role else []
    
    def has_permission(self, permission_name):
        """Check if user has a specific permission"""
        return permission_name in self.get_permissions()
    
    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role.name if self.role else None}')>"
