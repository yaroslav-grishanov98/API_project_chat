from sqlalchemy.orm import Session
from api_service.models.message import Message
from api_service.models.chat import Chat
from api_service.schemas.message import MessageCreate


def create_message(db: Session, chat_id: int, message: MessageCreate) -> Message:
    db_message = Message(text=message.text, chat_id=chat_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
