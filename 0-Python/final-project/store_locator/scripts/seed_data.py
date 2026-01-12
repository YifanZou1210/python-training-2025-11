# seed data in dbeare
from store_locator.app import create_app
from store_locator.app.extensions import db
from store_locator.app.models import User, Role
from datetime import datetime

app = create_app()

with app.app_context():
    print("Creating test users...")

    admin_role = Role.query.filter_by(name='admin').first()
    marketer_role = Role.query.filter_by(name='marketer').first()
    viewer_role = Role.query.filter_by(name='viewer').first()
    

    if not User.query.filter_by(email='admin@test.com').first():
        admin = User(email='admin@test.com', role=admin_role)
        admin.set_password('AdminTest123!')
        db.session.add(admin)
        print("✓ Admin user created: admin@test.com")
    

    if not User.query.filter_by(email='marketer@test.com').first():
        marketer = User(email='marketer@test.com', role=marketer_role)
        marketer.set_password('MarketerTest123!')
        db.session.add(marketer)
        print("✓ Marketer user created: marketer@test.com")
    
 
    if not User.query.filter_by(email='viewer@test.com').first():
        viewer = User(email='viewer@test.com', role=viewer_role)
        viewer.set_password('ViewerTest123!')
        db.session.add(viewer)
        print("✓ Viewer user created: viewer@test.com")
    
    db.session.commit()


    
    from app.stores.import_csv import import_stores_from_csv
    
    try:
        with open('data/stores_50.csv', 'rb') as f:
            result = import_stores_from_csv(f)
            
            if 'error' in result:
                print(f"✗ Import failed: {result['error']}")
            else:
                print(f"✓ Import successful!")
                print(f"  Total rows: {result['total_rows']}")
                print(f"  Created: {result['created']}")
                print(f"  Updated: {result['updated']}")
    except FileNotFoundError:
        print("  Please ensure the CSV file exists in the data/ directory")
    
