from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the chat (1-200 characters)")

    @field_validator('title')
    @classmethod
    def strip_title_whitespace(cls, v: str) -> str:
        return v.strip()

class ChatResponse(ChatCreate):
    id: int = Field(..., description="Unique ID of the chat")
    created_at: datetime = Field(..., description="Timestamp of when the chat was created")

    model_config = ConfigDict(from_attributes=True)

class ChatWithMessages(ChatResponse):
    messages: List['MessageResponse'] = Field(default_factory=list, description="List of messages in the chat")
