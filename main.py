from fastapi import FastAPI, Form
from pydantic import BaseModel
from models import create_db_and_tables, SessionDep
from models.message import Message
from sqlmodel import select

app = FastAPI()


class MessageForm(BaseModel):
    content: str

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# 
# Messages CRUD
# 

@app.get("/message")
def read_messages(session: SessionDep):
    return session.exec(select(Message)).all()


@app.get("/message/{message_id}")
def read_message_by_id(message_id: int):
    return None


@app.post("/message")
def create_message(message: Message, session: SessionDep) -> Message:
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


@app.delete("/message/{message_id}")
def delete_item_by_id(message_id: int):
    return None
