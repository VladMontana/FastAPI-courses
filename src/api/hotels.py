from datetime import date
from fastapi import APIRouter, Query, HTTPException
from fastapi_cache.decorator import cache

from src.core.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelsPatch
from src.exception import (
    HotelNotFoundException,
    CheckInDateAfterCheckOutDateException,
    CheckInDateEqualsCheckOutDateException
)

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.get("")
@cache(expire=60, namespace="hotels")
async def get_page_hotel(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None),
    title: str | None = Query(None),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    page = pagination.page or 1
    per_page = pagination.per_page or 5
    try:
        if date_from > date_to:
            raise CheckInDateAfterCheckOutDateException()
        if date_from == date_to:
            raise CheckInDateEqualsCheckOutDateException()
    except CheckInDateAfterCheckOutDateException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except CheckInDateEqualsCheckOutDateException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (page - 1),
    )


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete_constructor(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("/create")
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
