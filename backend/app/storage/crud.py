import hashlib
import json

def features_hash(features: list[str]) -> str:
    return hashlib.md5(json.dumps(sorted(features)).encode()).hexdigest()

def get_cached(location_key, features):
    h = features_hash(features)
    return db.query(CachedResult).filter_by(
        location_key=location_key,
        features_hash=h
    ).first()

def save_cached(location_key, features, result):
    record = CachedResult(
        location_key=location_key,
        features_hash=features_hash(features),
        result_json=result
    )
    db.add(record)
    db.commit()