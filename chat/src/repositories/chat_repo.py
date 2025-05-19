from sqlalchemy import select
from chat.src.repositories.base import SQLAlchemyRepo
from chat.src.db.models import Chat, Group, GroupMember


class ChatRepository(SQLAlchemyRepo[Chat]):
    model_cls = Chat

    async def get_all_members(self, chat_id) -> list[int]:
        stmt = (
            select(GroupMember.user_id)
            .join(Group, Group.id == GroupMember.group_id)
            .join(Chat, Group.id == Chat.group_id)
            .where(Chat.id == chat_id)
        )
        query = await self.session.execute(stmt)
        return query.scalars().all()

    async def get_all_by_user(self, user_id: int):
        stmt = (
            select(self.model_cls)
            .join(Group, Group.id == Chat.group_id)
            .join(GroupMember, Group.id == GroupMember.group_id)
            .where(GroupMember.user_id == user_id)
        )
        query = await self.session.execute(stmt)
        return query.scalars().all()

    async def add(
        self,
        chat_data: dict[str, any],
        group_data: dict[str, any],
        creator_id: int,
        members: list[int],
    ):
        group = Group(**group_data)
        self.session.add(group)
        await self.session.flush()

        chat_data["group_id"] = group.id
        chat = Chat(**chat_data)
        self.session.add(chat)

        members_ids = [
            GroupMember(group_id=group.id, user_id=member_id)
            for member_id in set(members + [creator_id])
        ]

        self.session.add_all(members_ids)
        await self.session.commit()
