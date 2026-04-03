from datetime import date
from fastapi import APIRouter, Query

from src.schemas.facilities import RoomsFacilitiesAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch
from src.core.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int, 
    db: DBDep, 
    date_from: date = Query(example=["2026-04-01"]), 
    date_to: date = Query(example=["2026-04-02"])
):
    return await db.rooms.get_filtered(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep): 
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    
    
@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    result = await db.rooms.add_constructor(_room_data)

    facilities_data = [RoomsFacilitiesAdd(room_id=result.id, facility_id=facility_id) for facility_id in data.facilities_ids]
    await db.rooms_facilities.add_bulk(facilities_data)
    await db.commit()
    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit_constructor(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}     


@router.patch("/{hotel_id}/rooms/{room_id}") 
async def edit_part_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit_constructor(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete_constructor(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

