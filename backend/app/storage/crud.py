import hashlib
import json
from app.storage.database import SessionLocal
from app.storage.models import CachedResult


def features_hash(features: list[str]) -> str:
    return hashlib.md5(json.dumps(sorted(features)).encode()).hexdigest()


def get_cached(location_key, features):
    db = SessionLocal()
    try:
        h = features_hash(features)
        return db.query(CachedResult).filter_by(
            location_key=location_key,
            features_hash=h
        ).first()
    finally:
        db.close()


def save_cached(location_key, features, result):
    db = SessionLocal()
    try:
        record = CachedResult(
            location_key=location_key,
            features_hash=features_hash(features),
            result_json=result
        )
        db.add(record)
        db.commit()
    finally:
        db.close()