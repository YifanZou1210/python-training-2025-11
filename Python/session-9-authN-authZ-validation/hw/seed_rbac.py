from flask import Flask 
from models import db 
from app import app
from model_rbac import User, Role, Permission 
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object('db_config')
db.init_app(app)

def seed_rbac_data():
    with app.app_context():
        db.drop_all()
        db.create_all() 

        permissions_data = [
                ('view_customers', 'View customer list and details'),
                ('create_customers', 'Create new customers'),
                ('update_customers', 'Update customer information'),
                ('delete_customers', 'Delete customers'),
                ('view_orders', 'View order list and details'),
                ('create_orders', 'Create new orders'),
                ('update_orders', 'Update order information'),
                ('delete_orders', 'Delete orders'),
                ('manage_users', 'Register new users and assign roles'),
            ]
        permissions = {}
        for name, desc in permissions_data:
                # create Permission ORM instance
                perm = Permission(name=name, description=desc)

                # add perm into session, sqlalchemy will add session into db when committed 
                db.session.add(perm)
                permissions[name] = perm # name: Permission
                print(f"  {name}")
        db.session.commit() 
        # admin role creation 
        admin_role = Role(
            name = "Admin", 
            description = "Full Access"
        )
        admin_role.permissions = list(permissions.values())
        db.session.add(admin_role)
        # sales role 
        sales_role = Role(
                name='Sales',
                description='Can manage customers and orders, but cannot delete or manage users'
            )
        sales_role.permissions = [
            permissions['view_customers'],
            permissions['create_customers'],
            permissions['update_customers'],
            permissions['view_orders'],
            permissions['create_orders'],
            permissions['update_orders'],
        ]
        db.session.add(sales_role)
        # viewer role 
        viewer_role = Role(
                name='Viewer',
                description='Read-only access to customers and orders'
            )
        viewer_role.permissions = [
            permissions['view_customers'],
            permissions['view_orders'],
        ]
        db.session.add(viewer_role)
        db.session.commit() 

        # Hash password
        password = 'Admin123'
        password_hash = generate_password_hash(password)
        
        admin_user = User(
            email='admin@example.com',
            password_hash=password_hash,
            name='System Admin',
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.commit()

        for role in [admin_role, sales_role, viewer_role]:
            print(f'{role.name}:{role.get_permission_names()}')

if __name__ == "__main__":
        seed_rbac_data()

