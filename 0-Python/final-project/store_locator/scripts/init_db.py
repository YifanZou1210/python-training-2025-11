
from store_locator.app import create_app
from store_locator.app.extensions import db
from store_locator.app.models import Role, Permission, Service
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import time

def create_database_if_not_exists():

    db_url = os.getenv('DATABASE_URL')

    parts = db_url.replace('postgresql://', '').split('/')
    db_name = parts[-1]  # store_locator
    conn_info = parts[0]  # postgres:mypassword@localhost:5433
    
    user_pass, host_port = conn_info.split('@')
    user, password = user_pass.split(':')
    host, port = host_port.split(':')
    

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres' 
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {db_name}')
            print(f"✓ Database '{db_name}' created")
        else:
            print(f"✓ Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        print("\nManual fix:")
        print(f"docker exec -it my-postgres psql -U postgres -c 'CREATE DATABASE {db_name};'")
        return False
    
    return True

app = create_app()

with app.app_context():
    print("="*60)
    print("Database Initialization (Docker Version)")
    print("="*60)
    
    # Step 1: 等待PostgreSQL启动
    print("\nWaiting for PostgreSQL to be ready...")
    max_retries = 10
    for i in range(max_retries):
        try:
            # 尝试连接
            db.engine.connect()
            print("✓ PostgreSQL is ready")
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"  Waiting... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("✗ PostgreSQL not responding")
                print(f"  Error: {e}")
                exit(1)
    
    # Step 2: 创建数据库
    if not create_database_if_not_exists():
        print("\n⚠️  Please create database manually and retry")
        exit(1)
    
    print("\nCreating database tables...")
    
    # Step 3: 创建所有表
    db.create_all()
    print("✓ Tables created")
    
    # ============================================================
    # 创建权限
    # ============================================================
    print("\nCreating permissions...")
    permissions_data = [
        {'name': 'view_stores', 'desc': 'View store information'},
        {'name': 'manage_stores', 'desc': 'Create, update, delete stores'},
        {'name': 'manage_users', 'desc': 'Manage user accounts'},
        {'name': 'import_data', 'desc': 'Import CSV data'}
    ]
    
    perms = {}
    for p_data in permissions_data:
        perm = Permission.query.filter_by(name=p_data['name']).first()
        if not perm:
            perm = Permission(name=p_data['name'])
            db.session.add(perm)
            print(f"  + {p_data['name']}")
        perms[p_data['name']] = perm
    
    db.session.commit()
    
    # ============================================================
    # 创建角色
    # ============================================================
    print("\nCreating roles...")
    
    # Admin角色
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin')
        admin_role.permissions = list(perms.values())
        db.session.add(admin_role)
        print("  + admin (all permissions)")
    
    # Marketer角色
    marketer_role = Role.query.filter_by(name='marketer').first()
    if not marketer_role:
        marketer_role = Role(name='marketer')
        marketer_role.permissions = [
            perms['view_stores'],
            perms['manage_stores'],
            perms['import_data']
        ]
        db.session.add(marketer_role)
        print("  + marketer (store management)")
    
    # Viewer角色
    viewer_role = Role.query.filter_by(name='viewer').first()
    if not viewer_role:
        viewer_role = Role(name='viewer')
        viewer_role.permissions = [perms['view_stores']]
        db.session.add(viewer_role)
        print("  + viewer (read-only)")
    
    db.session.commit()
    
    # ============================================================
    # 创建预定义服务
    # ============================================================
    print("\nCreating services...")
    services = [
        'pharmacy', 'pickup', 'returns', 'optical',
        'photo_printing', 'gift_wrapping', 'automotive', 'garden_center'
    ]
    
    for svc_name in services:
        svc = Service.query.filter_by(name=svc_name).first()
        if not svc:
            svc = Service(name=svc_name)
            db.session.add(svc)
            print(f"  + {svc_name}")
    
    db.session.commit()
    
    print("\n" + "="*60)
    print("✓ Database initialized successfully!")
    print("="*60)
    print("\nNext step: Run 'python scripts/seed_data.py' to load test data")