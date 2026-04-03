from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import database, models, auth
from .database import engine, get_db
from .routers import admin, content
import os

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ADQ Website Admin API", version="1.0.0")

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

@app.get("/health")
def health_check():
    return {"status": "healthy"}
