from datetime import date
from fastapi import APIRouter, Query, HTTPException
from fastapi_cache.decorator import cache

from src.core.dependencies import DBDep, PaginationDep
from src.schemas.hotels import HotelAdd, HotelsPatch
from src.exception import (
    HotelNotFoundException,
    CheckInDateAfterCheckOutDateException,
    CheckInDateEqualsCheckOutDateException,
)

from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_id_hotel(hotel_id)
    except HotelNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.get("")
@cache(expire=60, namespace="hotels")
async def get_page_hotel(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None),
    title: str | None = Query(None),
    date_from: date = Query(example=["2024-08-01"]),
    date_to: date = Query(example=["2024-08-10"]),
):
    try:
        if date_from > date_to:
            raise CheckInDateAfterCheckOutDateException()
        if date_from == date_to:
            raise CheckInDateEqualsCheckOutDateException()
    except CheckInDateAfterCheckOutDateException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except CheckInDateEqualsCheckOutDateException as e:
        raise HTTPException(status_code=400, detail=e.detail)

    return await HotelService(db).get_page(
        pagination=pagination,
        location=location,
        title=title,
        date_from=date_from,
        date_to=date_to,
    )


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_id_hotel(hotel_id=hotel_id)
    return {"status": "OK"}


@router.post("/create")
async def create_hotel(hotel_data: HotelAdd, db: DBDep):
    hotel = await HotelService(db).create_hotel(hotel_data=hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def part_edit_hotel(hotel_id: int, hotel_data: HotelsPatch, db: DBDep):
    await HotelService(db).part_edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    return {"status": "OK"}
