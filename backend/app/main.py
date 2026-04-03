from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import database, models, auth
from .database import engine, get_db
from .routers import admin, content
import os

# Ensure data directory exists (use absolute path for Render)
DATA_DIR = "/opt/render/project/src/backend/data"
os.makedirs(DATA_DIR, exist_ok=True)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize default data - runs at startup
def init_default_data():
    print("\n🔧 Starting database initialization...")
    db = database.SessionLocal()
    try:
        # Check if admin exists FIRST
        admin_count = db.query(models.Admin).count()
        print(f"📊 Found {admin_count} admin(s) in database")
        
        if admin_count == 0:
            print("🔑 No admin found, creating default admin...")
            from .auth import get_password_hash
            admin = models.Admin(
                username="admin",
                email="admin@adq.com",
                hashed_password=get_password_hash("admin123")
            )
            db.add(admin)
            db.commit()
            # Verify it was created
            db.refresh(admin)
            verify_admin = db.query(models.Admin).filter(models.Admin.username == "admin").first()
            if verify_admin:
                print("✓ Created default admin user (ID: " + str(verify_admin.id) + ")")
            else:
                print("❌ Admin creation failed!")
        else:
            print("✓ Admin user already exists")
        
        # Create default sections if none exist
        if db.query(models.Section).count() == 0:
            sections_data = [
                {
                    "section_key": "hero",
                    "title_ar": "التفاصيل المعمارية للمشاريع",
                    "title_en": "Architectural Details of Projects",
                    "subtitle_ar": "أدق التفاصيل في المقاولات المعمارية",
                    "subtitle_en": "The Finest Details In Architecture Contracting",
                },
                {
                    "section_key": "about",
                    "title_ar": "من نحن",
                    "title_en": "About Us",
                    "content_ar": "نحن شركة رائدة في مجال المقاولات المعمارية، متخصصون في تقديم حلول بناء وتصميم استثنائية. مع سنوات من الخبرة في الصناعة، نفخر بالاهتمام بالتفاصيل والالتزام بالتميز.",
                    "content_en": "We are a leading company in architectural contracting, specializing in delivering exceptional construction and design solutions. With years of industry experience, we pride ourselves on attention to detail and commitment to excellence.",
                },
                {
                    "section_key": "vision",
                    "title_ar": "رؤيتنا",
                    "title_en": "Our Vision",
                    "content_ar": "أن نكون الشركة الرائدة في مجال المقاولات المعمارية في المنطقة، معترف بنا لتميزنا في الجودة والابتكار والالتزام بتسليم المشاريع في الوقت المحدد.",
                    "content_en": "To be the leading architectural contracting company in the region, recognized for our excellence in quality, innovation, and commitment to timely project delivery.",
                },
                {
                    "section_key": "mission",
                    "title_ar": "رسالتنا",
                    "title_en": "Our Mission",
                    "content_ar": "تقديم خدمات مقاولات معمارية عالية الجودة تتجاوز توقعات عملائنا من خلال فريق محترف، وتقنيات متقدمة، والتزام راسخ بالسلامة والاستدامة.",
                    "content_en": "To deliver high-quality architectural contracting services that exceed our clients' expectations through professional expertise, advanced techniques, and unwavering commitment to safety and sustainability.",
                }
            ]
            for section_data in sections_data:
                section = models.Section(**section_data)
                db.add(section)
            db.commit()
            print("✓ Created default sections")
        
        # Create default services if none exist
        if db.query(models.Service).count() == 0:
            services_data = [
                {"title_ar": "البناء والتشييد", "title_en": "Construction"},
                {"title_ar": "التشطيب والديكور", "title_en": "Finishing"},
                {"title_ar": "التنسيق الطبيعي", "title_en": "Landscaping"},
                {"title_ar": "الترميم والتجديد", "title_en": "Restoration"},
                {"title_ar": "التصميم المعماري", "title_en": "Architectural Design"},
                {"title_ar": "البنية التحتية", "title_en": "Infrastructure"},
            ]
            for service_data in services_data:
                service = models.Service(**service_data)
                db.add(service)
            db.commit()
            print("✓ Created default services")
        
        # Create default contact info if none exists
        if db.query(models.ContactInfo).count() == 0:
            contact = models.ContactInfo(
                phone="+966 50 000 0000",
                whatsapp="+966 50 000 0000",
                email="info@adqdetails.com",
                location_ar="المملكة العربية السعودية",
                location_en="Saudi Arabia",
                address_ar="طريق الملك فهد، الرياض، المملكة العربية السعودية",
                address_en="King Fahd Road, Riyadh, Saudi Arabia",
                map_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3625.297214285714!2d46.675295!3d24.713552!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e2f03890d489399%3A0xba974d1c98e79157!2sRiyadh%20Saudi%20Arabia!5e0!3m2!1sen!2s!4v1234567890",
                social_whatsapp="+966500000000",
                social_instagram="https://instagram.com/adqdetails",
                social_twitter="https://twitter.com/adqdetails"
            )
            db.add(contact)
            db.commit()
            print("✓ Created default contact info")
        
        print("\n✅ Database initialized successfully!")
        print("\n📝 Default Admin Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Please change the password after first login!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

# Initialize on startup
init_default_data()

app = FastAPI(title="ADQ Website Admin API", version="1.0.0")

# Add a simple health check endpoint
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

@app.get("/debug")
def debug_info():
    """Check database path, admin users, and disk status"""
    import os
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
        db_file_exists = os.path.exists(db_path.replace("sqlite:///", ""))
        
        return {
            "database_url": db_path,
            "db_file_exists": db_file_exists,
            "admin_count": len(admins),
            "admins": admin_info,
            "pwd_context_scheme": "argon2"
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploaded images
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])

@app.get("/")
def read_root():
    return {"message": "ADQ Website Admin API"}
