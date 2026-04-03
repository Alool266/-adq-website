from sqlalchemy.orm import Session
from . import models, database
from .auth import get_password_hash

def init_db():
    db = database.SessionLocal()
    
    try:
        # Create default admin user
        admin = db.query(models.Admin).filter(models.Admin.username == "admin").first()
        if not admin:
            admin = models.Admin(
                username="admin",
                email="admin@adq.com",
                hashed_password=get_password_hash("admin123")
            )
            db.add(admin)
            print("✓ Created admin user: admin / admin123")
        
        # Create default sections based on the website
        sections_data = [
            {
                "section_key": "hero",
                "title_ar": "التفاصيل المعمارية للمشاريع",
                "title_en": "Architectural Details of Projects",
                "subtitle_ar": "أدق التفاصيل في المقاولات المعمارية",
                "subtitle_en": "The Finest Details In Architecture Contracting",
                "image_url": "/uploads/hero.jpg"
            },
            {
                "section_key": "about",
                "title_ar": "من نحن",
                "title_en": "About Us",
                "content_ar": "نحن شركة رائدة في مجال المقاولات المعمارية، متخصصون في تقديم حلول بناء وتصميم استثنائية. مع سنوات من الخبرة في الصناعة، نفخر بالاهتمام بالتفاصيل والالتزام بالتميز.",
                "content_en": "We are a leading company in architectural contracting, specializing in delivering exceptional construction and design solutions. With years of industry experience, we pride ourselves on attention to detail and commitment to excellence.",
                "image_url": "/uploads/about.jpg"
            },
            {
                "section_key": "vision",
                "title_ar": "رؤيتنا",
                "title_en": "Our Vision",
                "content_ar": "أن نكون الشركة الرائدة في مجال المقاولات المعمارية في المنطقة، معترف بنا لتميزنا في الجودة والابتكار والالتزام بتسليم المشاريع في الوقت المحدد.",
                "content_en": "To be the leading architectural contracting company in the region, recognized for our excellence in quality, innovation, and commitment to timely project delivery.",
                "image_url": None
            },
            {
                "section_key": "mission",
                "title_ar": "رسالتنا",
                "title_en": "Our Mission",
                "content_ar": "تقديم خدمات مقاولات معمارية عالية الجودة تتجاوز توقعات عملائنا من خلال فريق محترف، وتقنيات متقدمة، والتزام راسخ بالسلامة والاستدامة.",
                "content_en": "To deliver high-quality architectural contracting services that exceed our clients' expectations through professional expertise, advanced techniques, and unwavering commitment to safety and sustainability.",
                "image_url": None
            }
        ]
        
        for section_data in sections_data:
            section = db.query(models.Section).filter(models.Section.section_key == section_data["section_key"]).first()
            if not section:
                section = models.Section(**section_data)
                db.add(section)
                print(f"✓ Created section: {section_data['section_key']}")
        
        # Create default services
        services_data = [
            {
                "title_ar": "البناء والتشييد",
                "title_en": "Construction",
                "image_url": "/uploads/services/construction.jpg"
            },
            {
                "title_ar": "التشطيب والديكور",
                "title_en": "Finishing",
                "image_url": "/uploads/services/finishing.jpg"
            },
            {
                "title_ar": "التنسيق الطبيعي",
                "title_en": "Landscaping",
                "image_url": "/uploads/services/landscaping.jpg"
            },
            {
                "title_ar": "الترميم والتجديد",
                "title_en": "Restoration",
                "image_url": "/uploads/services/restoration.jpg"
            },
            {
                "title_ar": "التصميم المعماري",
                "title_en": "Architectural Design",
                "image_url": "/uploads/services/design.jpg"
            },
            {
                "title_ar": "البنية التحتية",
                "title_en": "Infrastructure",
                "image_url": "/uploads/services/infrastructure.jpg"
            }
        ]
        
        for service_data in services_data:
            service = db.query(models.Service).filter(
                models.Service.title_ar == service_data["title_ar"]
            ).first()
            if not service:
                service = models.Service(**service_data)
                db.add(service)
                print(f"✓ Created service: {service_data['title_en']}")
        
        # Create default contact info
        contact = db.query(models.ContactInfo).first()
        if not contact:
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
            print("✓ Created contact info")
        
        db.commit()
        print("\n✅ Database initialized successfully!")
        print("\n📝 Admin Login Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Please change the password after first login!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
