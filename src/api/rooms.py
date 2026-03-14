from fastapi import APIRouter

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
    

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker as session: 
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
    
    
@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add_constructor(_room_data)
        await session.commit()
    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit_constructor(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}     


@router.patch("/{hotel_id}/rooms/{room_id}") 
async def edit_part_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit_constructor(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete_constructor(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}