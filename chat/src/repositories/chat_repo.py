from chat.src.repositories.base import SQLAlchemyRepo
from chat.src.db.models import Chat


class ChatRepository(SQLAlchemyRepo[Chat]):
    model_cls = Chat
