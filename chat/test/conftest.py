import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from chat.src.db.models import Base,User
from chat.src.core.security import get_current_user  # или путь к get_current_user
from chat.src.db.dependencies import get_db
DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(DATABASE_URL_TEST, future=True)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function", autouse=True)
async def prepare_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await test_engine.dispose()

@pytest.fixture
async def db_session(test_engine):
    async_session = sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:

        yield session

        await session.rollback()

@pytest.fixture
def override_get_current_user():
    def _get_user():
        return User(id=1, name="Test User", email="test@example.com",hashed_password="test")
    return _get_user


@pytest.fixture
async def client(override_get_current_user,db_session):
    from httpx import ASGITransport
    from chat.main import app 

    app.dependency_overrides[get_current_user] = override_get_current_user
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db]=override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client