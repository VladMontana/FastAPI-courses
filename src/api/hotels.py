from datetime import date
from fastapi import APIRouter, Query

from src.core.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelsPatch

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)

@router.get("/paginated")
async def get_page_hotel(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None),
    title: str | None = Query(None),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10")
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )
        
        
@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete_constructor(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(hotel_data: HotelAdd, db: DBDep):
    hotel = await db.hotels.add_constructor(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit_constructor(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}   


@router.patch("/{hotel_id}")
async def part_edit_hotel(hotel_id: int, hotel_data: HotelsPatch, db: DBDep):
    await db.hotels.edit_constructor(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
    
