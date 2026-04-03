from datetime import date

from models.rooms import RoomsORM
from repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository

from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_filtered_rooms(self, hotel_id: int, date_from: date, date_to: date) -> int:
        query = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsORM.id.in_(query))
