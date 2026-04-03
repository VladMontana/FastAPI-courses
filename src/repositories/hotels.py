from datetime import date
from sqlalchemy import select, func

from models.rooms import RoomsORM
from repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel
    

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

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

