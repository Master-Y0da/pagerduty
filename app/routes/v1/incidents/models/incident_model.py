from sqlalchemy import Column, Integer, String
from app.config.db import Bases

class Incident(Bases["incidents"]):

    __tablename__ = 'incidents'
    __table_args__ = {'schema': 'incidents'}

    
    id = Column(Integer, primary_key=True, index=True)
    id_incident = Column(String(255), index=True)
    service = Column(String(255), index=True)
    summary = Column(String(255), index=True)
    status = Column(String(255), index=True)
