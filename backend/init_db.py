# Init DB - creates tables and admin user
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

print("🔧 Starting init_db.py...")

from database import engine, Base, SessionLocal
import models
from auth import get_password_hash

# Create all tables
print("🔧 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created!")

# Create admin user if not exists
print("🔧 Creating admin user...")
db = SessionLocal()
try:
    admin = db.query(models.Admin).first()
    if not admin:
        admin = models.Admin(
            username="admin",
            email="admin@adq.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created!")
    else:
        print("✅ Admin user already exists")
        print(f"   Username: {admin.username}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print("🔧 Done!")