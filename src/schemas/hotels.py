from pydantic import BaseModel
from typing import List

class Hotels(BaseModel):
    location: str
    title: str

