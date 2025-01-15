
from ..models import Incident
from ..serializers.team_serializer import TeamSerializer
from flask import current_app
from sqlalchemy import func
from typing import Dict, Any
import asyncio, httpx


class ApiClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        
    async def _get_incidents(self) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/api/v1/incidents/")
            response.raise_for_status()
            return response.json()
            
    def get_incidents(self) -> Dict[str, Any]:
        try:
            return asyncio.run(self._get_incidents())
        except Exception as e:
            current_app.logger.error(f"Error fetching incidents: {str(e)}")
            return {"error": str(e)}


class TeamData():

    def __init__(self,session):
        self.session = session

    def get_all(self):
        with self.session() as s:
            result = s.query(Incident).all()
            pydantic_result = [TeamSerializer.from_orm(item) for item in result]
            return [item.dict() for item in pydantic_result]
