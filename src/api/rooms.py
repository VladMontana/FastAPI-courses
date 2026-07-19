from datetime import date
from fastapi import APIRouter, Query, HTTPException

from src.schemas.facilities import RoomsFacilitiesAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch
from src.core.dependencies import DBDep
from src.exception import (
    CheckInDateAfterCheckOutDateException,
    CheckInDateEqualsCheckOutDateException,
    RoomNotFoundException,
    HotelNotFoundException
)

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example=["2026-04-01"]),
    date_to: date = Query(example=["2026-04-02"]),
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
    
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await db.rooms.get_room(hotel_id=hotel_id, id=room_id)
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, data: RoomAddRequest, db: DBDep):
    try:
        await db.hotels.get_hotel(hotel_id=hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        result = await db.rooms.add_constructor(_room_data)

        facilities_data = [
            RoomsFacilitiesAdd(room_id=result.id, facility_id=facility_id)
            for facility_id in data.facilities_ids
        ]
        await db.rooms_facilities.add_bulk(facilities_data)
        await db.commit()
    except HotelNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        await db.rooms.get_room(hotel_id=hotel_id, id=room_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await db.rooms.edit_constructor(_room_data, id=room_id, hotel_id=hotel_id)
        await db.rooms_facilities.set_room_facilities(
            room_id, facolities_ids=room_data.facilities_ids
        )
        await db.commit()
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_part_room(
    hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep
):
    try:
        await db.rooms.get_room(hotel_id=hotel_id, id=room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await db.rooms.edit_constructor(
            _room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if "facilities_ids" in _room_data_dict:
            await db.rooms_facilities.set_room_facilities(
                room_id, facolities_ids=_room_data_dict["facilities_ids"]
            )
        await db.commit()
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.rooms.get_room(hotel_id=hotel_id, id=room_id)
        await db.rooms.delete_constructor(id=room_id, hotel_id=hotel_id)
        await db.commit()
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}
