from starlette import status
from starlette.responses import Response

from app.models import SessionDep
from app.models.message import Message
from sqlmodel import select
from sqlalchemy.sql import text

from app import app


@app.get("/")
async def read_root():
    return "Hello, World!"


@app.get("/message")
async def get_messages(session: SessionDep):
    return session.exec(select(Message)).all()


@app.get("/message/{message_id}")
async def get_message_by_id(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return message


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: Message, session: SessionDep) -> Message:
    session.add(message)
    session.commit()
    session.refresh(message)

    return message


@app.put("/message/{message_id}")
async def update_item_by_id(message_id: int, new_message: Message, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    message.content = new_message.content
    session.commit()
    
    return {"new_content": new_message.content}


@app.delete("/message/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_by_id(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(message)

    return None
