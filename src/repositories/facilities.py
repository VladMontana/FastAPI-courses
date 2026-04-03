from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import FacilityAdd, RoomsFacilities

class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = FacilityAdd


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomsFacilities