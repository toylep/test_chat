import pytest
from httpx import AsyncClient
from chat.src.db.models import Chat, Group, GroupMember, User
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
async def test_add_chat(client: AsyncClient, db_session: AsyncSession, test_user):
    payload = {
        "name": "Test Chat",
        "is_group": True,
        "group": {
            "members": [1],
        }
    }

    response = await client.post("/api/v1/chat/", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Чат создан"

@pytest.mark.anyio
async def test_get_chats(client: AsyncClient, db_session: AsyncSession, test_user):
    group = Group(creator_id=test_user.id)
    db_session.add(group)
    await db_session.flush()

    chat = Chat(
        name="Test Chat", 
        is_group=True, 
        group_id=group.id
        )
    db_session.add(chat)

    member = GroupMember(group_id=group.id, user_id=test_user.id)
    db_session.add(member)
    await db_session.commit()

    response = await client.get("/api/v1/chat/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Test Chat"