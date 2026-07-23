from datetime import date

from src.services.base import BaseService
from src.core.dependencies import PaginationDep
from src.schemas.hotels import HotelAdd, HotelsPatch


class HotelService(BaseService):
    async def get_id_hotel(self, hotel_id: int):
        return await self.db.hotels.get_hotel(hotel_id=hotel_id)

    async def get_page(
        self,
        pagination: PaginationDep,
        location: str | None,
        title: str | None,
        date_from: date,
        date_to: date,
    ):
        page = pagination.page or 1
        per_page = pagination.per_page or 5

        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (page - 1),
        )

    async def delete_id_hotel(self, hotel_id: int):
        await self.db.hotels.delete_constructor(id=hotel_id)
        await self.db.commit()

    async def create_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add_constructor(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit_constructor(hotel_data, id=hotel_id)
        await self.db.commit()

    async def part_edit_hotel(self, hotel_id: int, hotel_data: HotelsPatch):
        await self.db.hotels.edit_constructor(
            hotel_data, exclude_unset=True, id=hotel_id
        )
        await self.db.commit()
