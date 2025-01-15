from pydantic import BaseModel, ConfigDict


class ServiceSerializer(BaseModel):
    id: int
    id_service: str
    name: str
    description: str=None
    status: str

    class Config:
        orm_mode = True

class ServiceGroupByIncidentSerializer(BaseModel):
    name: str
    count: int

    class Config:
        orm_mode = True