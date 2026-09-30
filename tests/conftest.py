import os
from pathlib import Path
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"
os.environ["DEMO_MODE"]="true"
os.environ["SECRET_KEY"]="test-secret-key"

import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    Path("test_pocketsmart.db").unlink(missing_ok=True)
