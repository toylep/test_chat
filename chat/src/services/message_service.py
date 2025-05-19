from chat.src.schemas.pagination import PaginatedResponse
from chat.src.services.base import BaseService
from chat.src.schemas.message import MessageCreateSchema, MessageResponseSchema
from chat.src.repositories.message_repo import MessageRepo


class MessageService(BaseService[MessageCreateSchema, MessageRepo]):
    response_schema = MessageResponseSchema

    async def get_message_history(self, chat_id: int, pagination: dict[str, int]):

        page = pagination.get("page")
        limit = pagination.get("limit")
        offset = (page - 1) * limit

        items = await self.repo.get_message_history(
            chat_id=chat_id, offset=offset, limit=limit
        )
        total = len(items)
        total_pages = (total + limit - 1) // limit

        items = [self.response_schema.model_validate(item.__dict__) for item in items]
        return PaginatedResponse[MessageResponseSchema](
            page=page, items=items, limit=limit, total_pages=total_pages, total=total
        )

    async def mark_messages_as_read(self, chat_id: int, user_id: int):
        return await self.repo.mark_messages_as_read(chat_id=chat_id, user_id=user_id)
