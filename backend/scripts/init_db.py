from app.storage.database import engine
from app.storage.models import Base

Base.metadata.create_all(bind=engine)
