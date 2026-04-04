from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import database, models, auth
from .database import engine, get_db
from .routers import admin, content
import os

app = FastAPI(title="ADQ Website Admin API", version="1.0.0")

# Include routers FIRST - before static files
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])

# Serve simple frontend-new at root
frontend_build = os.path.join(os.path.dirname(__file__), "../../frontend-new")
if os.path.exists(frontend_build):
    app.mount("/", StaticFiles(directory=frontend_build, html=True), name="frontend")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running"}

@app.get("/setup")
def setup_admin():
    """Visit this endpoint to create admin user if it doesn't exist"""
    db = database.SessionLocal()
    try:
        admin = db.query(models.Admin).first()
        if not admin:
            from .auth import get_password_hash
            admin = models.Admin(
                username="admin",
                email="admin@adq.com",
                hashed_password=get_password_hash("admin123")
            )
            db.add(admin)
            db.commit()
            return {"message": "Admin user created! You can now login with admin/admin123"}
        else:
            return {"message": "Admin user already exists"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/reset-admin")
def reset_admin():
    """Visit this endpoint to DELETE and RECREATE admin with argon2 hash"""
    db = database.SessionLocal()
    try:
        from .auth import get_password_hash
        # Delete ALL existing admins
        db.query(models.Admin).delete()
        db.commit()
        # Create fresh admin with argon2
        admin = models.Admin(
            username="admin",
            email="admin@adq.com",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin)
        db.commit()
        return {"message": "Admin RESET! Login with admin/admin123 (argon2 hash)"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/test-password")
def test_password():
    """Test if password verification works"""
    db = database.SessionLocal()
    try:
        admin = db.query(models.Admin).filter(models.Admin.username == "admin").first()
        if not admin:
            return {"error": "Admin not found"}

        from .auth import verify_password, get_password_hash

        # Test the password
        password = "admin123"
        is_valid = verify_password(password, admin.hashed_password)

        # Also test creating a new hash and verifying it
        new_hash = get_password_hash(password)
        new_hash_valid = verify_password(password, new_hash)

        return {
            "username": admin.username,
            "stored_hash": admin.hashed_password[:50] + "...",
            "test_password": password,
            "password_valid": is_valid,
            "new_hash_works": new_hash_valid,
            "pwd_context_scheme": "argon2"
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}
    finally:
        db.close()

@app.get("/debug")
def debug_info():
    """Check database path, admin users, and disk status"""
    db = database.SessionLocal()
    try:
        admins = db.query(models.Admin).all()
        admin_info = []
        for a in admins:
            admin_info.append({
                "id": a.id,
                "username": a.username,
                "email": a.email,
                "hash_prefix": a.hashed_password[:20] + "..." if a.hashed_password else None
            })

        db_path = database.SQLALCHEMY_DATABASE_URL

        return {
            "database_url": db_path,
            "admin_count": len(admins),
            "admins": admin_info,
            "pwd_context_scheme": "argon2"
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/")
def read_root():
    # Redirect to frontend
    return FileResponse(os.path.join(frontend_build, "index.html"))

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    try:
        models.Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Create admin user if not exists
        db = database.SessionLocal()
        try:
            admin = db.query(models.Admin).first()
            if not admin:
                from .auth import get_password_hash
                admin = models.Admin(
                    username="admin",
                    email="admin@adq.com",
                    hashed_password=get_password_hash("admin123")
                )
                db.add(admin)
                db.commit()
                print("✅ Admin user created in startup!")
            else:
                print("✅ Admin user already exists in startup")
        except Exception as e:
            print(f"❌ Error creating admin: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
