# scripts/update_passwords.py
from store_locator.run import app  # 直接导入你现有的 app
from store_locator.app.extensions import db
from store_locator.app.models import User


users_to_update = [
    {"email": "admin@test.com", "password": "AdminTest123!"},
    {"email": "marketer@test.com", "password": "MarketerTest123!"},
    {"email": "viewer@test.com", "password": "ViewerTest123!"},
]

with app.app_context():
    for u in users_to_update:
        email = u["email"]
        new_password = u["password"]
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"User {email} not found.")
        else:
            user.set_password(new_password)
            print(f"Updated password for {email}")
    
    # 一次性提交，避免多次 commit
    db.session.commit()
    print("All passwords updated successfully.")
