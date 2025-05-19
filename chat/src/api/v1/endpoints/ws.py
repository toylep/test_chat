from fastapi import APIRouter, Depends, WebSocket

from chat.src.core.security import get_current_user, get_current_user_in_ws
from chat.src.schemas.user import UserResponseSchema
from chat.src.services.dependencies import get_user_servise_ws, get_ws_service
from chat.src.services.user_service import UserService
from chat.src.services.ws_service import WSService


router = APIRouter()


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
):
    ws_service: WSService = get_ws_service()
    user_service: UserService = get_user_servise_ws()

    user = await get_current_user_in_ws(websocket, user_service)
    await ws_service.handle_websocket(websocket, user, chat_id)
