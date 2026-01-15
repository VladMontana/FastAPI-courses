from pydantic import BaseModel
from typing import List

class Hotels(BaseModel):
    id: int
    name: str
    title: str

class PaginatedResponse(BaseModel):
    total: int # сколько отелей находятся в списке
    page: int 
    per_page: int 
    data: List[Hotels]