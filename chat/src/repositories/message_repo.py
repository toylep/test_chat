from sqlalchemy import desc, select, update
from chat.src.repositories.base import SQLAlchemyRepo
from chat.src.db.models import Message


class MessageRepo(SQLAlchemyRepo[Message]):
    model_cls = Message

    async def mark_messages_as_read(self, chat_id: int, user_id: int):
        stmt = (
            update(Message)
            .where(Message.chat_id == chat_id)
            .where(Message.user_id != user_id)
            .where(Message.is_readed == False)
            .values(is_readed=True)
            .returning(self.model_cls.user_id)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().unique()

    async def get_message_history(self, chat_id: int, offset: int, limit: int):
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .offset(offset)
            .limit(limit)
            .order_by(desc(Message.timestampt))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
