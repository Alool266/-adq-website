-- Enable pgcrypto extension for password hashing
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Admins table
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    hashed_password VARCHAR(500) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Site settings table
CREATE TABLE IF NOT EXISTS site_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value_ar TEXT,
    value_en TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sections table
CREATE TABLE IF NOT EXISTS sections (
    id SERIAL PRIMARY KEY,
    section_key VARCHAR(100) UNIQUE NOT NULL,
    title_ar TEXT,
    title_en TEXT,
    subtitle_ar TEXT,
    subtitle_en TEXT,
    content_ar TEXT,
    content_en TEXT,
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title_ar VARCHAR(200) NOT NULL,
    title_en VARCHAR(200) NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    image_url VARCHAR(500) NOT NULL,
    category VARCHAR(50) DEFAULT '3d',
    is_active BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Services table
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    title_ar VARCHAR(200) NOT NULL,
    title_en VARCHAR(200) NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 0
);

-- Contact info table
CREATE TABLE IF NOT EXISTS contact_info (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(50),
    whatsapp VARCHAR(50),
    email VARCHAR(200),
    location_ar VARCHAR(200),
    location_en VARCHAR(200),
    address_ar TEXT,
    address_en TEXT,
    map_url TEXT,
    social_whatsapp VARCHAR(500),
    social_instagram VARCHAR(500),
    social_twitter VARCHAR(500)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_admins_username ON admins(username);
CREATE INDEX IF NOT EXISTS idx_sections_key ON sections(section_key);
CREATE INDEX IF NOT EXISTS idx_projects_category ON projects(category);
CREATE INDEX IF NOT EXISTS idx_services_order ON services("order");
