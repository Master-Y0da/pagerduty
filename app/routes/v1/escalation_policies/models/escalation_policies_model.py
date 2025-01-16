from sqlalchemy import Column, Integer, String, JSON
from app.config.db import Bases

class EscalationPolicies(Bases["escalation_policies"]):

    __tablename__ = 'escalation_policies'
    __table_args__ = {'schema': 'escalation_policies'}


    id = Column(Integer, primary_key=True, index=True)
    id_ep = Column(String(255), index=True)
    name = Column(String(255), index=True)
    type = Column(String(255), index=True)
    summary = Column(String(255), index=True)
    teams = Column(JSON, nullable=True)
    services = Column(JSON, nullable=True)
