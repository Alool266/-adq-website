# Init DB - creates tables and admin user
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database import engine, Base, SessionLocal
import models
from auth import get_password_hash

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created!")

# Create admin user if not exists
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
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()