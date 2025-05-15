from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from chat.src.core.config import settings

engine = create_async_engine(settings.db.connection_string())

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
