from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any


class ServiceSerializer(BaseModel):
    id: int
    id_service: str
    name: str
    description: str=None
    status: str
    team : Optional[List[Dict[str, Any]]]

    class Config:
        orm_mode = True

class ServiceGroupByIncidentSerializer(BaseModel):
    name: str
    count: int

    class Config:
        orm_mode = True
