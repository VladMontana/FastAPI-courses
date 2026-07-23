from fastapi import APIRouter

from src.schemas.facilities import FacilityAdd
from src.core.dependencies import DBDep

from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post("")
async def create_facility(db: DBDep, data: FacilityAdd):
    return await FacilitiesService(db).create_facilities(data=data)


@router.get("")
async def get_facilities(db: DBDep):
    return await FacilitiesService(db).get_facilities()


@router.get("/{facility_id}")
async def get_facility(facility_id: int, db: DBDep):
    facility = await FacilitiesService(db).get_facility(facility_id=facility_id)
    return {"status": "OK", "data": facility}
