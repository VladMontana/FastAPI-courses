from datetime import date
from sqlalchemy import select, func

from src.repositories.mapper.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel
from src.exception import ObjectNotFoundException, HotelNotFoundException

class HotelsRepository(BaseRepository[HotelsORM, Hotel]):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location: str | None = None,
        title: str | None = None,
        limit: int = 5,
        offset: int = 0,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
        )

        query = select(HotelsORM).filter(HotelsORM.id.in_(rooms_ids_to_get))
        if location:
            query = query.filter(
                func.lower(HotelsORM.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsORM.title).contains(title.strip().lower())
            )
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [
            self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()
        ]

    
    async def get_hotel(self, hotel_id: int):
        try:
            return await self.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException()
        