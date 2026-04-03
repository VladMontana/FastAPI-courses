from fastapi import APIRouter

from src.schemas.facilities import FacilityAddRequest, FacilityAdd
from src.core.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.post("")
async def create_facility(db: DBDep, data: FacilityAdd):
    facility = await db.facilities.add_constructor(data)
    await db.commit()
    return {"status": "OK", "data": facility}

@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()
    

@router.get("/{facility_id}")
async def get_facility(facility_id: int, db: DBDep):
    facility = await db.facilities.get_one_or_none(id=facility_id)
    return {"status": "OK", "data": facility}

@router.patch("/{facility_id}")
async def update_facility(facility_id: int, data: FacilityAdd, db: DBDep):
    facility = await db.facilities.update_one(id=facility_id, data=data)
    await db.commit()
    return {"status": "OK", "data": facility}