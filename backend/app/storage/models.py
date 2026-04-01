from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class CachedResult(Base):
    __tablename__ = "cached_results"

    id = Column(Integer, primary_key=True)
    location_key = Column(String, index=True)
    features_hash = Column(String, index=True)
    result_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)