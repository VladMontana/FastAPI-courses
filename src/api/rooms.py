from datetime import date
from fastapi import APIRouter, HTTPException

from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.core.dependencies import DBDep
from src.exception import (
    CheckInDateAfterCheckOutDateException,
    CheckInDateEqualsCheckOutDateException,
    RoomNotFoundException,
    HotelNotFoundException,
)
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date,
    date_to: date,
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

    return await RoomsService(db).get_rooms(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomsService(db).get_room_by_id(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, data: RoomAddRequest, db: DBDep):
    try:
        result = await RoomsService(db).create_room(hotel_id=hotel_id, data=data)
    except HotelNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    try:
        await RoomsService(db).edit_room(
            hotel_id=hotel_id, room_id=room_id, room_data=room_data
        )
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_part_room(
    hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep
):
    try:
        await RoomsService(db).edit_part_room(
            hotel_id=hotel_id, room_id=room_id, room_data=room_data
        )
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomsService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return {"status": "OK"}
