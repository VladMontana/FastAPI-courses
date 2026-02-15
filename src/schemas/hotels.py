from pydantic import BaseModel, Field

class Hotels(BaseModel):
    title: str
    location: str
    

class HotelsPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
    