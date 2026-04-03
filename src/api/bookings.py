from fastapi import APIRouter, HTTPException

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.core.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.post("")
async def add_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest):
    if booking_data.date_from >= booking_data.date_to:
        raise HTTPException(status_code=400, detail="Дата заезда не может быть больше даты выезда")
    
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    
    booked_count = await db.bookings.get_filtered_rooms(
        hotel_id=room.hotel_id, 
        date_from=booking_data.date_from, 
        date_to=booking_data.date_to
    )
    if booked_count >= room.quantity:
        raise HTTPException(status_code=400, detail="Комната уже забронирована")

    payload = BookingAdd(
        user_id=user_id,
        room_id=booking_data.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
        price=room.price
    )
    
    booking = await db.bookings.add_constructor(payload)
    await db.commit()
    return {"status": "OK", "booking": booking}

