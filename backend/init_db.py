# Init DB - just create tables (admin user created on /setup)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database import engine, Base
import models

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Database tables created!")