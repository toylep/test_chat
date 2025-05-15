from fastapi import APIRouter, WebSocket


router = APIRouter()


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    service: ChatService = Depends(get_chat_service),
    user: User = Depends(get_current_user),
):
    await service.handle_websocket(websocket, user, chat_id)
