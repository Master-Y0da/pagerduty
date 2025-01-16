from sqlalchemy import Column, Integer, String, JSON
from app.config.db import Bases

class Service(Bases["services"]):

    __tablename__ = 'services'
    __table_args__ = {'schema': 'services'}


    id = Column(Integer, primary_key=True, index=True)
    id_service = Column(String(255), index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    status = Column(String(255), index=True)
    team = Column(JSON, nullable=True)
