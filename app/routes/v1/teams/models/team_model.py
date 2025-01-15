from sqlalchemy import Column, Integer, String
from app.config.db import Bases

class Teams(Bases["teams"]):

    __tablename__ = 'teams'
    __table_args__ = {'schema': 'teams'}

    
    id = Column(Integer, primary_key=True, index=True)
    id_team = Column(String(255), index=True)
    type = Column(String(255), index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    summary = Column(String(255), index=True)
