from pydantic import BaseModel
import os
from typing import Optional

class PlantRequest(BaseModel):
    plant_type: str

class PlantCreate(BaseModel):
    name: str
    plot_index: int
    plant_type: str
    user_id: str
    stage: str
    room: Optional[str] = None
    plant_start: str
    last_watered: str