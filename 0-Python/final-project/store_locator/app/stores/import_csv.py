"""
CSV批量导入逻辑
支持创建和更新（Upsert）
"""
import pandas as pd
from store_locator.app.models import Store, Service
from store_locator.app.extensions import db

def import_stores_from_csv(file):
    """
    从CSV文件导入店铺数据
    
    行为:
    - 如果store_id存在 → UPDATE
    - 如果store_id不存在 → CREATE
    
    参数:
        file: CSV文件对象
    
    返回:
    {
        "success": true,
        "total_rows": 50,
        "created": 30,
        "updated": 20
    }
    或
    {
        "error": "...",
        "failed_rows": [...]
    }
    """
    
    # Step 1: 读取CSV
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return {'error': f'Invalid CSV file: {str(e)}'}
    
    # Step 2: 验证CSV结构
    required_cols = [
        'store_id', 'name', 'store_type', 'status', 'latitude', 'longitude',
        'address_street', 'address_city', 'address_state', 'address_postal_code',
        'phone', 'services'
    ]
    
    missing = set(required_cols) - set(df.columns)
    if missing:
        return {'error': f'Missing required columns: {list(missing)}'}
    
    # Step 3: 逐行处理
    created_count = 0
    updated_count = 0
    failed = []
    
    try:
        # 开启事务
        for idx, row in df.iterrows():
            try:
                # 检查店铺是否存在
                store = Store.query.filter_by(store_id=row['store_id']).first()
                
                if store:
                    # UPDATE逻辑
                    store.name = row['name']
                    store.store_type = row['store_type']
                    store.status = row['status']
                    store.phone = row['phone']
                    store.hours_mon = row.get('hours_mon')
                    store.hours_tue = row.get('hours_tue')
                    store.hours_wed = row.get('hours_wed')
                    store.hours_thu = row.get('hours_thu')
                    store.hours_fri = row.get('hours_fri')
                    store.hours_sat = row.get('hours_sat')
                    store.hours_sun = row.get('hours_sun')
                    updated_count += 1
                else:
                    # CREATE逻辑
                    store = Store(
                        store_id=row['store_id'],
                        name=row['name'],
                        store_type=row['store_type'],
                        status=row['status'],
                        latitude=row['latitude'],
                        longitude=row['longitude'],
                        address_street=row['address_street'],
                        address_city=row['address_city'],
                        address_state=row['address_state'],
                        address_postal_code=row['address_postal_code'],
                        address_country=row.get('address_country', 'USA'),
                        phone=row['phone'],
                        hours_mon=row.get('hours_mon'),
                        hours_tue=row.get('hours_tue'),
                        hours_wed=row.get('hours_wed'),
                        hours_thu=row.get('hours_thu'),
                        hours_fri=row.get('hours_fri'),
                        hours_sat=row.get('hours_sat'),
                        hours_sun=row.get('hours_sun')
                    )
                    db.session.add(store)
                    created_count += 1
                
                # 处理服务（清空旧的，添加新的）
                store.services = []
                if pd.notna(row['services']):
                    for svc_name in row['services'].split('|'):
                        svc_name = svc_name.strip()
                        svc = Service.query.filter_by(name=svc_name).first()
                        if not svc:
                            svc = Service(name=svc_name)
                            db.session.add(svc)
                            db.session.flush()  # 获取service ID
                        store.services.append(svc)
                
            except Exception as e:
                failed.append({
                    'row': idx + 2,  # CSV行号（从1开始，跳过header）
                    'store_id': row.get('store_id', 'N/A'),
                    'error': str(e)
                })
        
        # Step 4: 检查是否有失败
        if failed:
            db.session.rollback()
            return {
                'error': 'Import failed',
                'failed_rows': failed
            }
        
        # Step 5: 提交事务
        db.session.commit()
        
        return {
            'success': True,
            'total_rows': len(df),
            'created': created_count,
            'updated': updated_count
        }
        
    except Exception as e:
        db.session.rollback()
        return {'error': f'Import failed: {str(e)}'}