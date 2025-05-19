from pydantic import BaseModel


class PaginatedResponse[ItemResponse](BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    limit: int
    total_pages: int
