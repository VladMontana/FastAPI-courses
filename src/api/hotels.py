from fastapi import HTTPException, APIRouter, Query

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotels, HotelsPATCH, PaginatedResponse

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("/")
def print_hotels():
    return hotels


@router.get("/paginated", response_model=PaginatedResponse)
async def get_page_hotel(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_


@router.put("/{hotel_id}")
async def update_hotel(
    hotel_id: int, 
    hotel_data: Hotels
):  
    if not hotel_data.title.strip():
        raise HTTPException(400, "Title cannot be empty")
    if not hotel_data.name.strip():
        raise HTTPException(400, "Name cannot be empty")
    
    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        raise HTTPException(400, "Hotel is not found")
    
    hotel["title"] = hotel_data.title.strip()
    hotel["name"] = hotel_data.name.strip()
    
    return {"message": "Hotel updated", "hotel": hotel}


@router.patch("/{hotel_id}")
async def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelsPATCH
):
    if hotel_data.title is None and hotel_data.name is None:
        raise HTTPException(400, "Title and name cannot be None")
    
    if hotel_data.title is not None and not hotel_data.title.strip():
        raise HTTPException(400, "Title cannot be empty")
    if hotel_data.name is not None and not hotel_data.title.strip():
        raise HTTPException(400, "Name cannot be empty")

    hotel = next((h for h in hotels if h["id"] == hotel_id), None)
    if not hotel:
        raise HTTPException(400, "Hotel isn`t found")
    
    if hotel_data.title is not None:
        hotel["title"] = hotel_data.title.strip()
    if hotel_data.name is not None:
        hotel["name"] = hotel_data.name.strip()
        
    return {"message": "Hotel partially update", "hotel": hotel}
    

