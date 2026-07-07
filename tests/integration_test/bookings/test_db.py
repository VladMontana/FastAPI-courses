from datetime import date

from src.schemas.bookings import BookingAdd


async def test_crud_booking(db, register_user):
    users = await db.users.get_all()
    user = users[0].id
    rooms = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user,
        room_id=rooms,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100
    )
    new_booking = await db.bookings.add_constructor(booking_data)
    
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id
    
    update_date = date(year=2024, month=8, day=25)
    update_booking_data = BookingAdd(
        user_id=user,
        room_id=rooms,
        date_from=date(year=2024, month=8, day=10),
        date_to=update_date,
        price=100
    )
    await db.bookings.edit_constructor(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.room_id == new_booking.room_id
    assert updated_booking.user_id == new_booking.user_id
    assert update_booking_data.date_to == update_date
    
    deleted_booking = await db.bookings.delete_constructor(id=new_booking.id)
    assert not deleted_booking
    await db.rollback()
    