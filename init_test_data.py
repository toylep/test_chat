import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import asyncio
from chat.src.db.models import User, Chat, Group, GroupMember, Message
from chat.src.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def init_data():
    async with AsyncSessionLocal() as session: 

        # Создание пользователя
        user = User(
            name="Test User",
            email="test@example.com",
            hashed_password="hashed"
        )
        session.add(user)
        await session.flush()

        group = Group(creator_id=user.id)
        session.add(group)
        await session.flush()

        group_member = GroupMember(group_id=group.id, user_id=user.id)
        session.add(group_member)

        chat = Chat(name="Test Chat", is_group=True, group_id=group.id)
        session.add(chat)
        await session.flush()

        messages = [
            Message(chat_id=chat.id, user_id=user.id, text="Hello!"),
            Message(chat_id=chat.id, user_id=user.id, text="How are you?")
        ]
        session.add_all(messages)

        await session.commit()
        print("✅ Тестовые данные успешно добавлены.")


if __name__ == "__main__":
    asyncio.run(init_data())