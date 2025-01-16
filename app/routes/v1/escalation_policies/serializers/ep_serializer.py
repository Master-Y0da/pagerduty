
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class EscalationPolicySerializer(BaseModel):

    id: int
    id_ep: str
    name: str
    summary: str=None
    teams: Optional[List[Dict[str, Any]]]
    services: Optional[List[Dict[str, Any]]]

    class Config:
        orm_mode = True

class EpCountSerializer(BaseModel):

    count: int
    ep: List[EscalationPolicySerializer]

    class Config:
        orm_mode = True
