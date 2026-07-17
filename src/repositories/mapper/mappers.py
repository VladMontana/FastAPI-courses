from src.repositories.mapper.base import DataMapper

from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomsFacilities

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesORM
from src.models.facilities import RoomsFacilitiesORM


class HotelDataMapper(DataMapper[HotelsORM, Hotel]):
    db_model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper[RoomsORM, Room]):
    db_model = RoomsORM
    schema = Room


class RoomDataWithRelsMapper(DataMapper[RoomsORM, RoomWithRels]):
    db_model = RoomsORM
    schema = RoomWithRels


class UserDataMapper(DataMapper[UsersORM, User]):
    db_model = UsersORM
    schema = User


class BookingDataMapper(DataMapper[BookingsOrm, Booking]):
    db_model = BookingsOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper[FacilitiesORM, Facility]):
    db_model = FacilitiesORM
    schema = Facility


class RoomsFacilitiesDataMapper(DataMapper[RoomsFacilitiesORM, RoomsFacilities]):
    db_model = RoomsFacilitiesORM
    schema = RoomsFacilities
