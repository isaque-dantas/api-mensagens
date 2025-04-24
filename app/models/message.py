from sqlmodel import Field, SQLModel

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
