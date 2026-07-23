from datetime import date
from src.services.base import BaseService
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch
from src.schemas.facilities import RoomsFacilitiesAdd


class RoomsService(BaseService):
    async def get_rooms(self, hotel_id: int, date_from: date, date_to: date):
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room_by_id(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_room(hotel_id=hotel_id, id=room_id)

    async def create_room(self, hotel_id: int, data: RoomAddRequest):
        await self.db.hotels.get_hotel(hotel_id=hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        result = await self.db.rooms.add_constructor(_room_data)

        facilities_data = [
            RoomsFacilitiesAdd(room_id=result.id, facility_id=facility_id)
            for facility_id in data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(facilities_data)
        await self.db.commit()
        return result

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        await self.db.rooms.get_room(hotel_id=hotel_id, id=room_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit_constructor(_room_data, id=room_id, hotel_id=hotel_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id, facolities_ids=room_data.facilities_ids
        )
        await self.db.commit()

    async def edit_part_room(
        self, hotel_id: int, room_id: int, room_data: RoomPatchRequest
    ):
        await self.db.rooms.get_room(hotel_id=hotel_id, id=room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit_constructor(
            _room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facolities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await self.db.rooms.get_room(hotel_id=hotel_id, id=room_id)
        await self.db.rooms.delete_constructor(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
