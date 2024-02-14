import sqlite3
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .model import Base, Event, Ticket


SQLALCHEMY_DATABAE_URL =  "sqlite:///./events_db"
engine = create_engine(SQLALCHEMY_DATABAE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Information needed to create an event
class EventCreate(BaseModel):
    title: str
    location: str
    start_date: str
    end_date: str
    available_tickets: int


# Information needed to create a ticket
class TicketCreate(BaseModel):
    event_id: int
    customer_name: str
    customer_email: str


# Initialize database connection
def get_db():
    database=SessionLocal()
    yield database
    database.close()


# Create event
@app.post("/events")
async def create_event(event: EventCreate, database: Session=Depends(get_db))-> Event:
    db_event = Event(event)
    database.add(db_event)
    database.commit()
    database.refresh(db_event)
    return db_event

@app.delete("/events/{event_id}")
def delete_event(event_id: int, database: Session=Depends(get_db))-> Event:
    event = database.query(Event).filter(Event.id==event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    database.delete(event)
    database.commit()
    return event

# Get event by id
@app.get("/events/{event_id}")
async def get_event(event_id: int, database: Session=Depends(get_db))-> Event:
    event = database.query(Event).filter(Event.id==event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    return event


# Get all events
@app.get("/events")
async def get_all_events(database: Session=Depends(get_db))-> list[Event]:
    events = database.query(Event).all()
    return events


# Book ticket
@app.post("/tickets")
async def book_ticket(ticket: TicketCreate, database: Session=Depends(get_db))-> Ticket:
    event = database.query(Event).filter(Event.id==ticket.event_id).first()
    if not event:
            raise HTTPException(status_code=404, detail="event not found")
    if event.available_tickets < 1:
        raise HTTPException(status_code=400, detail="No available tickets.")

    db_ticket = Ticket(**ticket)
    database.add(db_ticket)
    database.commit()
    database.refresh(db_ticket)
    return db_ticket


# Get event by id
@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int, database: Session=Depends(get_db)) -> Ticket:
    ticket = database.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
 
def main():
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
