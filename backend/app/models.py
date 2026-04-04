from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SiteSetting(Base):
    __tablename__ = "site_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    value_ar = Column(Text, nullable=True)
    value_en = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Section(Base):
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    section_key = Column(String, unique=True, index=True, nullable=False)  # e.g., 'hero', 'about', 'services'
    title_ar = Column(Text, nullable=True)
    title_en = Column(Text, nullable=True)
    subtitle_ar = Column(Text, nullable=True)
    subtitle_en = Column(Text, nullable=True)
    content_ar = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title_ar = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    image_url = Column(String, nullable=False)
    category = Column(String, default="3d")  # 3d, construction, finished
    is_active = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    title_ar = Column(String, nullable=False)
    title_en = Column(String, nullable=False)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    order = Column(Integer, default=0)

class ContactInfo(Base):
    __tablename__ = "contact_info"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, nullable=True)
    whatsapp = Column(String, nullable=True)
    email = Column(String, nullable=True)
    location_ar = Column(String, nullable=True)
    location_en = Column(String, nullable=True)
    address_ar = Column(String, nullable=True)
    address_en = Column(String, nullable=True)
    map_url = Column(String, nullable=True)
    social_whatsapp = Column(String, nullable=True)
    social_instagram = Column(String, nullable=True)
    social_twitter = Column(String, nullable=True)
