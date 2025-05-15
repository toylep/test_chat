from chat.src.services.base import BaseService
from chat.src.schemas.chat import ChatCreateSchema, ChatResponseSchema
from chat.src.repositories.chat_repo import ChatRepository


class ChatService(BaseService[ChatCreateSchema, ChatRepository]):
    response_schema = ChatResponseSchema
