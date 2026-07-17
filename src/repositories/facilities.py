from sqlalchemy import select, delete, insert

from src.repositories.mapper.mappers import (
    FacilitiesDataMapper,
    RoomsFacilitiesDataMapper,
)
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facility, RoomsFacilities


class FacilitiesRepository(BaseRepository[FacilitiesORM, Facility]):
    model = FacilitiesORM
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository[RoomsFacilitiesORM, RoomsFacilities]):
    model = RoomsFacilitiesORM
    mapper = RoomsFacilitiesDataMapper

    async def set_room_facilities(self, room_id: int, facolities_ids: list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        current_facilities_id = list(res.scalars().all())
        ids_to_delete: list[int] = list(
            set(current_facilities_id) - set(facolities_ids)
        )
        ids_to_insert: list[int] = list(
            set(facolities_ids) - set(current_facilities_id)
        )

        if ids_to_delete:
            delete_m2m_stmt = delete(self.model).where(
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)
            )
            await self.session.execute(delete_m2m_stmt)

        if ids_to_insert:
            insert_m2m_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
            )
            await self.session.execute(insert_m2m_stmt)
