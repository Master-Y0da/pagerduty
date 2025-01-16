from pydantic import BaseModel


class TeamSerializer(BaseModel):

    id: int
    name: str
    #members: str

    class Config:
        orm_mode = True
