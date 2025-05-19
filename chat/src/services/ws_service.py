from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict
from chat.src.schemas.message import MessageCreateSchema, MessageResponseSchema
from chat.src.schemas.user import UserResponseSchema
from chat.src.services.chat_service import ChatService
from chat.src.services.message_service import MessageService
from chat.src.utils.async_lock import AsyncLock
from fastapi.encoders import jsonable_encoder


class WSService:
    """
    Менеджер для работы с вебсокетами
    Сейчас используется статическое поле, которое можно заменить каким-нибудь redis
    """

    active_connections: dict[int, dict[int, WebSocket]] = defaultdict(dict)

    def __init__(self, message_service: MessageService, chat_service: ChatService):
        self.message_service = message_service
        self.chat_service = chat_service

    async def handle_websocket(
        self,
        websocket: WebSocket,
        user: UserResponseSchema,
        chat_id: int,
    ):
        await websocket.accept()
        self.active_connections[chat_id][user.id] = websocket

        try:
            while True:
                text = await websocket.receive_text()
                message = await self._process_message(text, user.id, chat_id)
                await self._broadcast(chat_id=chat_id, message=message)
        except WebSocketDisconnect:
            del self.active_connections[chat_id][user.id]
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def _process_message(
        self, text: str, user_id: int, chat_id: int
    ) -> MessageResponseSchema:
        async with AsyncLock():
            return await self.message_service.add(
                MessageCreateSchema(text=text, chat_id=chat_id, user_id=user_id)
            )

    async def _broadcast(self, chat_id: int, message: MessageResponseSchema):
        participant_ids = await self.chat_service.get_all_members(chat_id)
        message_json = jsonable_encoder(message.model_dump())

        for user_id in participant_ids:
            websocket = self.active_connections.get(chat_id, {}).get(user_id)
            if websocket:
                await websocket.send_json(message_json)
