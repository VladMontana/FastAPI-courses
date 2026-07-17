from pydantic import BaseModel


class FacilityAddRequest(BaseModel):
    title: str


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int


class RoomsFacilitiesAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacilities(RoomsFacilitiesAdd):
    id: int
    facility_id: int
