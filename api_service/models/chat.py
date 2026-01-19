from sqlalchemy import Column, Integer, String, DateTime, func, desc
from sqlalchemy.orm import relationship
from api_service.core.database import Base
from .message import Message


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chat(id={self.id}, title='{self.title}')>"
