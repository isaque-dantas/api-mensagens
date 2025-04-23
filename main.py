from fastapi import FastAPI, Form
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()


class MessageForm(BaseModel):
    content: str


class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Messages CRUD

@app.get("/message")
def read_messages():
    return None


@app.get("/message/{message_id}")
def read_message_by_id(message_id: int):
    return None


@app.post("/message")
def create_item():
    return None


@app.delete("/message/{message_id}")
def delete_item_by_id(message_id: int):
    return None
