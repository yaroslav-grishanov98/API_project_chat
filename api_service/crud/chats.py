from api_service.schemas.chat import ChatCreate
from typing import Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from api_service.models.chat import Chat
from api_service.models.message import Message


def create_chat(db: Session, chat: ChatCreate) -> Chat:
    db_chat = Chat(title=chat.title)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat(db: Session, chat_id: int) -> Optional[Chat]:
    return db.query(Chat).filter(Chat.id == chat_id).first()

def get_chat_with_messages(db: Session, chat_id: int, limit: int = 20) -> Optional[Chat]:
    chat_obj = db.query(Chat).filter(Chat.id == chat_id).first()

    if chat_obj:
        latest_messages = (
            db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(desc(Message.created_at), desc(Message.id))
            .limit(limit)
            .all()
        )

        chat_obj.messages = latest_messages

    return chat_obj

def delete_chat(db: Session, chat_id: int):
    chat_obj = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat_obj:
        db.delete(chat_obj)
        db.commit()
        return True
    return False
