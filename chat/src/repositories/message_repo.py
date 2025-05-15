from chat.src.repositories.base import SQLAlchemyRepo
from chat.src.db.models import Message


class MessageRepo(SQLAlchemyRepo[Message]):
    models = Message
