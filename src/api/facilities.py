from fastapi import APIRouter
from redis import RedisError

from src.connectors.redis_manager import redis_manager
from src.schemas.facilities import FacilityAdd
from src.core.dependencies import DBDep
from src.utils.json_converter import to_json, from_json

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("")
async def create_facility(db: DBDep, data: FacilityAdd):
    facility = await db.facilities.add_constructor(data)
    await db.commit()

    try:
        await redis_manager.delete("facilities")
    except RedisError:
        pass

    return facility


@router.get("")
async def get_facilities(db: DBDep):
    try:
        facilities_from_cache = await redis_manager.get("facilities")
    except RedisError:
        facilities_from_cache = None

    if facilities_from_cache is not None:
        return from_json(facilities_from_cache)

    facilities = await db.facilities.get_all()

    facilities_schemas = [f.model_dump() for f in facilities]
    facilities_json = to_json(facilities_schemas)

    try:
        await redis_manager.set("facilities", facilities_json, expire=3600)
    except RedisError:
        pass

    return facilities


@router.get("/{facility_id}")
async def get_facility(facility_id: int, db: DBDep):
    facility = await db.facilities.get_one_or_none(id=facility_id)
    return {"status": "OK", "data": facility}


# @router.patch("/{facility_id}")
# async def update_facility(facility_id: int, data: FacilityAdd, db: DBDep):
#     facility = await db.facilities.update_one(id=facility_id, data=data)
#     await db.commit()
#     return {"status": "OK", "data": facility}
