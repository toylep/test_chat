from enum import Enum

from fastapi import Depends

from chat.src.db.dependencies import get_db
from chat.src.repositories.chat_repo import ChatRepository
from chat.src.repositories.message_repo import MessageRepo
from chat.src.repositories.user_repo import UserRepository
from chat.src.db.session import AsyncSessionLocal

from chat.src.services.chat_service import ChatService
from chat.src.services.message_service import MessageService
from chat.src.services.user_service import UserService
from chat.src.services.ws_service import WSService
from chat.src.repositories.dependencies import (
    get_chat_repo,
    get_message_repo,
    get_user_repo,
)


def get_chat_service(repo: ChatRepository = Depends(get_chat_repo)) -> ChatService:
    return ChatService(repo)


def get_message_service(
    repo: MessageRepo = Depends(get_message_repo),
) -> MessageService:
    return MessageService(repo)


def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo)


# WS


def get_ws_service() -> WSService:
    """
    Внутри вебсокетов нельзя использовать DI поэтому создается такой костыль
    """
    return WSService(
        message_service=MessageService(MessageRepo(AsyncSessionLocal())),
        chat_service=ChatService(ChatRepository(AsyncSessionLocal())),
    )


def get_user_servise_ws() -> UserService:
    """
    Внутри вебсокетов нельзя использовать DI поэтому создается такой костыль
    """
    return UserService(UserRepository(AsyncSessionLocal()))
