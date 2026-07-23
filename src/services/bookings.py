from src.services.base import BaseService
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.exception import CheckInDateAfterCheckOutDateException, RoomNotFoundException


class BookingsService(BaseService):
    async def get_bookings_by_id(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def add_booking(self, user_id: int, booking_data: BookingAddRequest):
        if booking_data.date_from >= booking_data.date_to:
            raise CheckInDateAfterCheckOutDateException()

        room = await self.db.rooms.get_room_by_id(id=booking_data.room_id)
        if not room:
            raise RoomNotFoundException()

        payload = BookingAdd(
            user_id=user_id,
            room_id=booking_data.room_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            price=room.price,
        )

        booking = await self.db.bookings.add_booking(payload)

        return booking
