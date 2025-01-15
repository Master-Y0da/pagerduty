from pydantic import BaseModel


class IncidentSerializer(BaseModel):

    id: int
    id_incident: str
    service: str
    summary: str
    status: str

    class Config:
        orm_mode = True

class IncidentsGroupByServiceSerializer(BaseModel):

    service: str
    count: int

    class Config:
        orm_mode = True

class IncidentsGroupByServiceAndStatusSerializer(BaseModel):

    incident: str
    service: str
    status: str
    count: int

    class Config:
        orm_mode = True