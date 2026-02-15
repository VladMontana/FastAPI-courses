from fastapi import APIRouter, Query

from src.schemas.dependencies import PaginationDep

from src.schemas.hotels import Hotels, HotelsPatch
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)

@router.get("/paginated")
async def get_page_hotel(
    pagination: PaginationDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page or 5,
            offset=per_page * (pagination.page - 1)
        )
        
        
@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete_constructor(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data: Hotels):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add_constructor(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: Hotels):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit_constructor(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}   


@router.patch("/{hotel_id}")
async def part_edit_hotel(hotel_id: int, hotel_data: HotelsPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit_constructor(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
    
