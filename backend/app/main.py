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

# Get the root directory (project root, not backend)
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Serve CSS
@app.get("/styles.css")
def serve_css():
    return FileResponse(os.path.join(root_dir, "styles.css"))

# Serve JS
@app.get("/script.js")
def serve_js():
    return FileResponse(os.path.join(root_dir, "script.js"))

# Serve images
@app.get("/images/{path:path}")
def serve_image(path: str):
    image_path = os.path.join(root_dir, "images", path)
    return FileResponse(image_path)

# Serve original website at root
@app.get("/")
def serve_original():
    return FileResponse(os.path.join(root_dir, "index.html"))

# Serve simple admin panel at /admin
admin_dir = os.path.join(root_dir, "frontend-new")
app.mount("/admin", StaticFiles(directory=admin_dir, html=True), name="admin")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running"}

# Auto-seed database on startup - always seed to ensure we have data
@app.on_event("startup")
async def startup_seed():
    from .database import SessionLocal
    import models
    db = SessionLocal()
    try:
        print("🔧 Checking database content...")
        # Always try to add default content if not exists
        hero = db.query(models.Section).filter_by(section_key="hero").first()
        if not hero:
            print("🔧 Seeding sections...")
            hero = models.Section(section_key="hero", title_ar="التفاصيل المعمارية للمشاريع", title_en="Architectural Details of Projects", subtitle_ar="تصاميم ثلاثية الأبعاد | بناء | تشطيب", subtitle_en="3D Designs | Construction | Finishing", is_active=True, order=1)
            db.add(hero)
            about = models.Section(section_key="about", title_ar="من نحن", title_en="About Us", content_ar="نحن متخصصون في تقديم حلول معمارية متكاملة", content_en="We specialize in comprehensive architectural solutions", is_active=True, order=2)
            db.add(about)
            services = models.Section(section_key="services", title_ar="خدماتنا", title_en="Our Services", content_ar="تصاميم ثلاثية الأبعاد - بناء - تشطيبات", content_en="3D Designs - Construction - Finishing", is_active=True, order=3)
            db.add(services)
        
        contact = db.query(models.ContactInfo).first()
        if not contact:
            print("🔧 Seeding contact...")
            contact = models.ContactInfo(phone="+966500000000", whatsapp="+966500000000", email="info@adqdetails.com", location_ar="الرياض", location_en="Riyadh")
            db.add(contact)
        
        services_count = db.query(models.Service).count()
        if services_count == 0:
            print("🔧 Seeding services...")
            for s in [("تصاميم ثلاثية الأبعاد", "3D Designs", 1), ("تحت البناء", "Under Construction", 2), ("مشاريع منجزة", "Finished Projects", 3)]:
                db.add(models.Service(title_ar=s[0], title_en=s[1], order=s[2], is_active=True))
        
        projects_count = db.query(models.Project).count()
        if projects_count == 0:
            print("🔧 Seeding projects...")
            for p in [("فيلا سكنية", "Residential Villa", "3d"), ("مبنى تجاري", "Commercial Building", "construction"), ("شقة فاخرة", "Luxury Apartment", "finished")]:
                db.add(models.Project(title_ar=p[0], title_en=p[1], category=p[2], is_active=True))
        
        db.commit()
        print("✅ Database ready!")
    except Exception as e:
        print(f"Seed error: {e}")
        db.rollback()
    finally:
        db.close()

@app.get("/seed")
def seed_database():
    """Visit this to manually seed the database"""
    from .database import SessionLocal
    import models
    db = SessionLocal()
    try:
        # Check if we need to seed
        hero = db.query(models.Section).filter_by(section_key="hero").first()
        if not hero:
            print("🔧 Seeding...")
            hero = models.Section(section_key="hero", title_ar="التفاصيل المعمارية للمشاريع", title_en="Architectural Details of Projects", subtitle_ar="تصاميم ثلاثية الأبعاد | بناء | تشطيب", subtitle_en="3D Designs | Construction | Finishing", is_active=True, order=1)
            db.add(hero)
            about = models.Section(section_key="about", title_ar="من نحن", title_en="About Us", content_ar="نحن متخصصون في تقديم حلول معمارية متكاملة", content_en="We specialize in comprehensive architectural solutions", is_active=True, order=2)
            db.add(about)
            services = models.Section(section_key="services", title_ar="خدماتنا", title_en="Our Services", content_ar="تصاميم ثلاثية الأبعاد - بناء - تشطيبات", content_en="3D Designs - Construction - Finishing", is_active=True, order=3)
            db.add(services)
            contact = models.ContactInfo(phone="+966500000000", whatsapp="+966500000000", email="info@adqdetails.com", location_ar="الرياض", location_en="Riyadh")
            db.add(contact)
            for s in [("تصاميم ثلاثية الأبعاد", "3D Designs", 1), ("تحت البناء", "Under Construction", 2), ("مشاريع منجزة", "Finished Projects", 3)]:
                db.add(models.Service(title_ar=s[0], title_en=s[1], order=s[2], is_active=True))
            for p in [("فيلا سكنية", "Residential Villa", "3d"), ("مبنى تجاري", "Commercial Building", "construction"), ("شقة فاخرة", "Luxury Apartment", "finished")]:
                db.add(models.Project(title_ar=p[0], title_en=p[1], category=p[2], is_active=True))
            db.commit()
            return {"status": "Database seeded!"}
        return {"status": "Already seeded"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

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
