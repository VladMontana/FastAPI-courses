from datetime import date

from sqlalchemy import select

from src.models.rooms import RoomsORM
from src.repositories.mapper.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking, BookingAdd
from src.models.bookings import BookingsOrm
from src.utils.exception import RoomFullyBookedException


class BookingsRepository(BaseRepository[BookingsOrm, Booking]):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_filtered_rooms(
        self, hotel_id: int, date_from: date, date_to: date
    ) -> int:
        query = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return len(await self.get_filtered(RoomsORM.id.in_(query)))

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    # HTTP 409 - Надо ставить
    async def add_booking(self, booking_data: BookingAdd):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=booking_data.date_from, date_to=booking_data.date_to
        )

        query = select(RoomsORM).filter(
            RoomsORM.id == booking_data.room_id, RoomsORM.id.in_(rooms_ids_to_get)
        )
        result = await self.session.execute(query)
        room = result.scalars().one_or_none()

        if room is None:
            raise RoomFullyBookedException

        return await self.add_constructor(booking_data)
