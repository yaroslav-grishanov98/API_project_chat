from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class MessageCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Content of the message (1-5000 characters)")


class MessageResponse(MessageCreate):
    id: int = Field(..., description="Unique ID of the message")
    chat_id: int = Field(..., description="ID of the chat to which the message belongs")
    created_at: datetime = Field(..., description="Timestamp of when the message was created")

    model_config = ConfigDict(from_attributes=True)
