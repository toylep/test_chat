from chat.src.services.base import BaseService
from chat.src.schemas.message import MessageCreateSchema, MessageResponseSchema
from chat.src.repositories.message_repo import MessageRepo


class MessageService(BaseService[MessageCreateSchema, MessageRepo]):
    response_schema = MessageResponseSchema
