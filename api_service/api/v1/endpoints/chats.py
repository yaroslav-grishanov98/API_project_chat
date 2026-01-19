from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from api_service.core.database import get_db
from api_service.schemas.chat import ChatCreate, ChatResponse, ChatWithMessages
from api_service.schemas.message import MessageCreate, MessageResponse
from api_service.crud import chats as crud_chats
from api_service.crud import messages as crud_messages

router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_new_chat(chat_in: ChatCreate, db: Session = Depends(get_db)):
    """Создает новый чат с указанным заголовком"""
    db_chat = crud_chats.create_chat(db=db, chat=chat_in)
    return db_chat


@router.post("/{chat_id}/messages/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message_to_chat(
        chat_id: int,
        message_in: MessageCreate,
        db: Session = Depends(get_db)
):
    """Отправляет новое сообщение в существующий чат"""
    chat_exists = crud_chats.get_chat(db, chat_id=chat_id)
    if not chat_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found"
        )

    db_message = crud_messages.create_message(db=db, chat_id=chat_id, message=message_in)
    return db_message


@router.get("/{chat_id}", response_model=ChatWithMessages)
def get_chat_and_messages(
        chat_id: int,
        limit: int = Query(20, ge=1, le=100, description="Number of latest messages to retrieve"),
        db: Session = Depends(get_db)
):
    """Получает информацию о чате и последние сообщения"""
    db_chat = crud_chats.get_chat_with_messages(db, chat_id=chat_id, limit=limit)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found"
        )
    return db_chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_chat(chat_id: int, db: Session = Depends(get_db)):
    """Удаляет чат и все связанные с ним сообщения"""
    deleted = crud_chats.delete_chat(db=db, chat_id=chat_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat with id {chat_id} not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
