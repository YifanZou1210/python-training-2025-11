"""
手动导入services关联
前提：stores表已通过DBeaver导入
"""
import pandas as pd
import os
from store_locator.app import create_app
from store_locator.app.extensions import db
from store_locator.app.models import Store, Service

app = create_app()

with app.app_context():
    # 读取CSV
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # # BASE_DIR -> final-project/store_locator

    # PROJECT_ROOT = os.path.dirname(BASE_DIR)
    # # PROJECT_ROOT -> final-project

    # csv_path = os.path.join(PROJECT_ROOT, 'data', 'stores_50.csv')

    df = pd.read_csv('store_locator/data/stores_50.csv')
    
    for _, row in df.iterrows():
        store = Store.query.filter_by(store_id=row['store_id']).first()
        if not store:
            print(f"✗ Store {row['store_id']} not found")
            continue
        
        # 清空现有服务
        store.services = []
        
        # 添加新服务
        if pd.notna(row['services']):
            for svc_name in row['services'].split('|'):
                svc = Service.query.filter_by(name=svc_name.strip()).first()
                if svc:
                    store.services.append(svc)
        
        print(f"✓ Updated services for {row['store_id']}")
    
    db.session.commit()
    print("\n✓ All services imported!")