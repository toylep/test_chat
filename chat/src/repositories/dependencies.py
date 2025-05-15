from enum import Enum

from fastapi import Depends
from chat.src.repositories.chat_repo import ChatRepository
from chat.src.repositories.message_repo import MessageRepo
from chat.src.repositories.user_repo import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from chat.src.db.dependencies import get_db


def get_chat_repo(session: AsyncSession = Depends(get_db)) -> ChatRepository:
    return ChatRepository(session)


def get_message_repo(session: AsyncSession = Depends(get_db)) -> MessageRepo:
    return MessageRepo(session)


def get_user_repo(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)
