from chat.src.repositories.base import SQLAlchemyRepo
from chat.src.db.models import Group


class GroupRepository(SQLAlchemyRepo[Group]):
    model_cls = Group
