from main import app, get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool)
Base.metadata.create_all(bind=engine)
TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

def override_get_db():
    database = TestSessionLocal()
    yield database
    database.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_event()->None:
    event_data = {
        "title": "Christmas Block Party",
        "location": "Town center, Rockledge",
        "start_date": "2023-12-19 14:00:00",
        "end_date": "2023-12-22 18:00:00",
        "available_tickets": 20
    }
    response = client.post("/events", json=event_data)
    event = response.json()
    
    assert (
        'id' in event
        and event['title'] == event_data['title']
        and event['location'] == event_data['location']
        and event['available_tickets'] == event_data['available_tickets']
    )
    