from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import uuid
from .. import database, models, auth
from ..database import get_db

router = APIRouter()

# Pydantic schemas
class SiteSettingUpdate(BaseModel):
    value_ar: Optional[str] = None
    value_en: Optional[str] = None

class SiteSettingResponse(BaseModel):
    id: int
    key: str
    value_ar: Optional[str]
    value_en: Optional[str]
    
    class Config:
        from_attributes = True

class SectionCreate(BaseModel):
    section_key: str
    title_ar: Optional[str] = None
    title_en: Optional[str] = None
    subtitle_ar: Optional[str] = None
    subtitle_en: Optional[str] = None
    content_ar: Optional[str] = None
    content_en: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True
    order: int = 0

class SectionUpdate(BaseModel):
    title_ar: Optional[str] = None
    title_en: Optional[str] = None
    subtitle_ar: Optional[str] = None
    subtitle_en: Optional[str] = None
    content_ar: Optional[str] = None
    content_en: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None

class SectionResponse(BaseModel):
    id: int
    section_key: str
    title_ar: Optional[str]
    title_en: Optional[str]
    subtitle_ar: Optional[str]
    subtitle_en: Optional[str]
    content_ar: Optional[str]
    content_en: Optional[str]
    image_url: Optional[str]
    is_active: bool
    order: int
    
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    title_ar: str
    title_en: str
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    image_url: str
    category: str = "3d"
    is_active: bool = True
    order: int = 0

class ProjectUpdate(BaseModel):
    title_ar: Optional[str] = None
    title_en: Optional[str] = None
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None

class ProjectResponse(BaseModel):
    id: int
    title_ar: str
    title_en: str
    description_ar: Optional[str]
    description_en: Optional[str]
    image_url: str
    category: str
    is_active: bool
    order: int
    
    class Config:
        from_attributes = True

class ServiceCreate(BaseModel):
    title_ar: str
    title_en: str
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    image_url: str
    is_active: bool = True
    order: int = 0

class ServiceUpdate(BaseModel):
    title_ar: Optional[str] = None
    title_en: Optional[str] = None
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None

class ServiceResponse(BaseModel):
    id: int
    title_ar: str
    title_en: str
    description_ar: Optional[str]
    description_en: Optional[str]
    image_url: str
    is_active: bool
    order: int
    
    class Config:
        from_attributes = True

class ContactInfoUpdate(BaseModel):
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    location_ar: Optional[str] = None
    location_en: Optional[str] = None
    address_ar: Optional[str] = None
    address_en: Optional[str] = None
    map_url: Optional[str] = None
    social_whatsapp: Optional[str] = None
    social_instagram: Optional[str] = None
    social_twitter: Optional[str] = None

class ContactInfoResponse(BaseModel):
    id: int
    phone: Optional[str]
    whatsapp: Optional[str]
    email: Optional[str]
    location_ar: Optional[str]
    location_en: Optional[str]
    address_ar: Optional[str]
    address_en: Optional[str]
    map_url: Optional[str]
    social_whatsapp: Optional[str]
    social_instagram: Optional[str]
    social_twitter: Optional[str]
    
    class Config:
        from_attributes = True

class ImageUploadResponse(BaseModel):
    url: str
    filename: str

# ============ SITE SETTINGS ============
@router.get("/settings", response_model=List[SiteSettingResponse])
def get_settings(db: Session = Depends(get_db)):
    return db.query(models.SiteSetting).all()

@router.get("/settings/{key}", response_model=SiteSettingResponse)
def get_setting(key: str, db: Session = Depends(get_db)):
    setting = db.query(models.SiteSetting).filter(models.SiteSetting.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@router.put("/settings/{key}", response_model=SiteSettingResponse)
def update_setting(key: str, setting_data: SiteSettingUpdate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    setting = db.query(models.SiteSetting).filter(models.SiteSetting.key == key).first()
    if not setting:
        setting = models.SiteSetting(key=key, **setting_data.model_dump())
        db.add(setting)
    else:
        for field, value in setting_data.model_dump().items():
            if value is not None:
                setattr(setting, field, value)
        setting.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(setting)
    return setting

# ============ SECTIONS ============
@router.get("/sections", response_model=List[SectionResponse])
def get_sections(db: Session = Depends(get_db)):
    return db.query(models.Section).order_by(models.Section.order).all()

@router.get("/sections/{section_key}", response_model=SectionResponse)
def get_section(section_key: str, db: Session = Depends(get_db)):
    section = db.query(models.Section).filter(models.Section.section_key == section_key).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.post("/sections", response_model=SectionResponse)
def create_section(section_data: SectionCreate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    section = models.Section(**section_data.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section

@router.put("/sections/{section_key}", response_model=SectionResponse)
def update_section(section_key: str, section_data: SectionUpdate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    section = db.query(models.Section).filter(models.Section.section_key == section_key).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    for field, value in section_data.model_dump(exclude_unset=True).items():
        setattr(section, field, value)
    section.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(section)
    return section

@router.delete("/sections/{section_id}")
def delete_section(section_id: int, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    section = db.query(models.Section).filter(models.Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    db.delete(section)
    db.commit()
    return {"message": "Section deleted"}

# ============ PROJECTS ============
@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).order_by(models.Project.order).all()

@router.post("/projects", response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    project = models.Project(**project_data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    return project

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}

# ============ SERVICES ============
@router.get("/services", response_model=List[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).order_by(models.Service.order).all()

@router.post("/services", response_model=ServiceResponse)
def create_service(service_data: ServiceCreate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    service = models.Service(**service_data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@router.put("/services/{service_id}", response_model=ServiceResponse)
def update_service(service_id: int, service_data: ServiceUpdate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    for field, value in service_data.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service

@router.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    return {"message": "Service deleted"}

# ============ CONTACT INFO ============
@router.get("/contact", response_model=ContactInfoResponse)
def get_contact_info(db: Session = Depends(get_db)):
    contact = db.query(models.ContactInfo).first()
    if not contact:
        contact = models.ContactInfo()
        db.add(contact)
        db.commit()
        db.refresh(contact)
    return contact

@router.put("/contact", response_model=ContactInfoResponse)
def update_contact_info(contact_data: ContactInfoUpdate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    contact = db.query(models.ContactInfo).first()
    if not contact:
        contact = models.ContactInfo(**contact_data.model_dump())
        db.add(contact)
    else:
        for field, value in contact_data.model_dump(exclude_unset=True).items():
            setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact

# ============ IMAGE UPLOAD ============
@router.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...), current_admin: models.Admin = Depends(auth.get_current_admin)):
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join("uploads", filename)
    
    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return ImageUploadResponse(url=f"/uploads/{filename}", filename=filename)
