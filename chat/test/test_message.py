import pytest
from httpx import AsyncClient
from chat.src.db.models import User, Chat, Group, GroupMember, Message
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def test_user(db_session: AsyncSession):
    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password="test"
        )
    db_session.add(user)
    await db_session.commit()
    return user

@pytest.mark.anyio
async def test_get_history(client: AsyncClient, db_session: AsyncSession,test_user):
    
    group = Group(creator_id=test_user.id)
    db_session.add(group)
    await db_session.flush()  

    chat = Chat(name="Test Chat", is_group=False, group_id=group.id)
    db_session.add(chat)

    group_member = GroupMember(group_id=group.id, user_id=test_user.id)
    db_session.add(group_member)
    await db_session.flush()  


    message1 = Message(
        chat_id=chat.id,
        user_id=test_user.id,
        text="Hello",
        is_readed=False
    )
    message2 = Message(
        chat_id=chat.id,
        user_id=test_user.id,
        text="World",
        is_readed=False
    )
    db_session.add_all([message1, message2])
    await db_session.commit()

    response = await client.get("/api/v1/messages/history/1?page=1&limit=10")
    assert response.status_code == 200
    json_data = response.json()
    assert "items" in json_data
    assert isinstance(json_data["items"], list)



@pytest.mark.anyio
async def test_mark_messages_as_read(client: AsyncClient, db_session: AsyncSession,test_user):
    # Аналогично добавим пользователя, чат и сообщения

    group = Group(creator_id=test_user.id)
    db_session.add(group)
    await db_session.flush()

    chat = Chat(name="Test Chat", is_group=False, group_id=group.id)
    db_session.add(chat)

    group_member = GroupMember(group_id=group.id, user_id=test_user.id)
    db_session.add(group_member)
    await db_session.flush()
    message1 = Message(
        chat_id=chat.id,
        user_id=test_user.id,
        text="Hello",
        is_readed=False
    )
    db_session.add(message1)
    await db_session.commit()

    response = await client.get("/api/v1/messages/read/1")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

