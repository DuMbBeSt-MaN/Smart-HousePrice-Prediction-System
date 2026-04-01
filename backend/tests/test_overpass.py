from app.services.overpass_client import query_nearby

def test_hospitals():
    assert query_nearby("hospital", 34.05, -118.24) >= 0