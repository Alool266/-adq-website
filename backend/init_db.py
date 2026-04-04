# Init DB - creates tables, admin user, and default content
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

    # Seed sections
    print("🔧 Seeding sections...")
    
    # Hero section
    hero = db.query(models.Section).filter_by(section_key="hero").first()
    if not hero:
        hero = models.Section(
            section_key="hero",
            title_ar="التفاصيل المعمارية للمشاريع",
            title_en="Architectural Details of Projects",
            subtitle_ar="تصاميم ثلاثية الأبعاد | بناء | تشطيب",
            subtitle_en="3D Designs | Construction | Finishing",
            is_active=True,
            order=1
        )
        db.add(hero)
    
    # About section
    about = db.query(models.Section).filter_by(section_key="about").first()
    if not about:
        about = models.Section(
            section_key="about",
            title_ar="من نحن",
            title_en="About Us",
            content_ar="نحن متخصصون في تقديم حلول architectural متكاملة تشمل التصميم ثلاثي الأبعاد، البناء، والتشطيبات الداخلية والخارجية. نتميز بدقة التنفيذ وجودة المواد.",
            content_en="We specialize in providing comprehensive architectural solutions including 3D design, construction, and interior/exterior finishing. We are distinguished by execution accuracy and quality materials.",
            is_active=True,
            order=2
        )
        db.add(about)

    # Services section
    services = db.query(models.Section).filter_by(section_key="services").first()
    if not services:
        services = models.Section(
            section_key="services",
            title_ar="خدماتنا",
            title_en="Our Services",
            content_ar="تصاميم ثلاثية الأبعاد - بناء وتأهيل - تشطيبات فاخرة",
            content_en="3D Designs - Construction & Rehabilitation - Luxury Finishing",
            is_active=True,
            order=3
        )
        db.add(services)

    db.commit()
    print("✅ Sections seeded!")

    # Seed contact info
    print("🔧 Seeding contact info...")
    contact = db.query(models.ContactInfo).first()
    if not contact:
        contact = models.ContactInfo(
            phone="+966500000000",
            whatsapp="+966500000000",
            email="info@adqdetails.com",
            location_ar="الرياض، المملكة العربية السعودية",
            location_en="Riyadh, Saudi Arabia",
            social_whatsapp="https://wa.me/966500000000"
        )
        db.add(contact)
        db.commit()
        print("✅ Contact info seeded!")

    # Seed services
    print("🔧 Seeding services...")
    service_list = [
        {"title_ar": "تصاميم ثلاثية الأبعاد", "title_en": "3D Designs", "order": 1},
        {"title_ar": "تحت البناء", "title_en": "Under Construction", "order": 2},
        {"title_ar": "مشاريعFinished", "title_en": "Finished Projects", "order": 3}
    ]
    for s in service_list:
        existing = db.query(models.Service).filter_by(title_en=s["title_en"]).first()
        if not existing:
            service = models.Service(
                title_ar=s["title_ar"],
                title_en=s["title_en"],
                order=s["order"],
                is_active=True
            )
            db.add(service)
    db.commit()
    print("✅ Services seeded!")

    # Seed projects
    print("🔧 Seeding sample projects...")
    project_list = [
        {"title_ar": "فيلا سكنية", "title_en": "Residential Villa", "category": "3d"},
        {"title_ar": "مبنى تجاري", "title_en": "Commercial Building", "category": "construction"},
        {"title_ar": "شقة فاخرة", "title_en": "Luxury Apartment", "category": "finished"}
    ]
    for p in project_list:
        existing = db.query(models.Project).filter_by(title_en=p["title_en"]).first()
        if not existing:
            project = models.Project(
                title_ar=p["title_ar"],
                title_en=p["title_en"],
                category=p["category"],
                image_url="",
                is_active=True
            )
            db.add(project)
    db.commit()
    print("✅ Projects seeded!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()

print("🔧 Done!")