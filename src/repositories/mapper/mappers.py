from src.repositories.mapper.base import DataMapper

from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesORM

class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel
    
class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room
    
    
class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsORM
    schema = RoomWithRels
    
    
class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User
    
    
class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    dm_model = FacilitiesORM
    schema = Facility