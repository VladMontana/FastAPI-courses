from redis import RedisError

from src.connectors.redis_manager import redis_manager
from src.services.base import BaseService
from src.schemas.facilities import FacilityAdd
from src.utils.json_converter import to_json, from_json


class FacilitiesService(BaseService):
    async def create_facilities(self, data: FacilityAdd):
        facility = await self.db.facilities.add_constructor(data)
        await self.db.commit()

        try:
            await redis_manager.delete("facilities")
        except RedisError:
            pass

        return facility

    async def get_facilities(self):
        try:
            facilities_from_cache = await redis_manager.get("facilities")
        except RedisError:
            facilities_from_cache = None

        if facilities_from_cache is not None:
            return from_json(facilities_from_cache)

        facilities = await self.db.facilities.get_all()

        facilities_schemas = [f.model_dump() for f in facilities]
        facilities_json = to_json(facilities_schemas)

        try:
            await redis_manager.set("facilities", facilities_json, expire=3600)
        except RedisError:
            pass

        return facilities

    async def get_facility(self, facility_id: int):
        facility = await self.db.facilities.get_one_or_none(id=facility_id)
        return facility
