from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from chat.src.schemas.user import UserResponseSchema
from chat.src.services.base import BaseService
from chat.src.schemas.chat import ChatCreateSchema, ChatResponseSchema
from chat.src.repositories.chat_repo import ChatRepository


class ChatService(BaseService[ChatCreateSchema, ChatRepository]):
    response_schema = ChatResponseSchema

    async def get_all_by_user(self, user: UserResponseSchema) -> JSONResponse:
        items = await self.repo.get_all_by_user(user.id)
        return [self.response_schema.model_validate(item.__dict__) for item in items]

    async def get_all_members(self, chat_id: int) -> list[int]:
        return await self.repo.get_all_members(chat_id)

    async def add(
        self, dto: ChatCreateSchema, user: UserResponseSchema
    ) -> JSONResponse:

        chat_data = dto.model_dump()
        group_data = chat_data.pop("group")
        group_data["creator_id"] = user.id
        members = group_data.pop("members")

        if dto.is_group is False:
            if len(set(members + [user.id])) > 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "У личного чата не может быть более двух участников"
                    },
                )

        await self.repo.add(
            chat_data=chat_data,
            group_data=group_data,
            creator_id=user.id,
            members=members,
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"message": "Чат создан"}
        )
