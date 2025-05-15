from chat.src.repositories.base import SQLAlchemyRepo
from chat.src.db.models import User


class UserRepository(SQLAlchemyRepo[User]):
    model_cls = User

    async def get_by_email(self, email: str):
        return await self.get_with_filters({"email": email}, return_single=True)

    