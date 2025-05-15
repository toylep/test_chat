from fastapi import WebSocket, WebSocketDisconnect


class WSService:
    def __init__(self, message_repo: Mes):
        self.message_repo = message_repo
        self.active_connections = {}

    async def handle_websocket(self, websocket: WebSocket, user: User):
        await websocket.accept()
        self.active_connections[user.id] = websocket

        try:
            while True:
                data = await websocket.receive_json()
                message = await self._process_message(data, user)
                await self._broadcast(message)
        except WebSocketDisconnect:
            del self.active_connections[user.id]

    async def _process_message(self, data: dict, user: User) -> Message:
        async with async_lock:  # Для предотвращения дублирования
            return await self.message_repo.create(
                chat_id=data["chat_id"], sender_id=user.id, text=data["text"]
            )
