from fastapi import APIRouter, HTTPException

from src.schemas.bookings import BookingAddRequest
from src.core.dependencies import DBDep, UserIdDep
from src.exception import (
    CheckInDateAfterCheckOutDateException,
    RoomNotFoundException,
    RoomFullyBookedException,
)
from src.services.bookings import BookingsService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingsService(db).get_bookings_by_id(user_id=user_id)


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_all_bookings()


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    try:
        booking = await BookingsService(db).add_booking(
            user_id=user_id, booking_data=booking_data
        )
        await db.commit()
        return {"status": "OK", "booking": booking}
    except CheckInDateAfterCheckOutDateException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except RoomNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except RoomFullyBookedException as e:
        raise HTTPException(status_code=409, detail=e.detail)
