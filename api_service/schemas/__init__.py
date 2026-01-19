from .chat import ChatCreate, ChatResponse, ChatWithMessages
from .message import MessageCreate, MessageResponse

ChatWithMessages.model_rebuild()