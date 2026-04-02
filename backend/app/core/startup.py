# app/core/startup.py

from app.storage.database import engine
from app.storage.models import Base

def on_startup():
    """
    Placeholder for:
    - DB init
    - Scheduler start
    """
    print("🚀 Application started")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("📊 Database tables created/verified")