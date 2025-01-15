
from ..models import Service
from ..serializers.ServiceSerializer import ServiceSerializer, ServiceGroupByIncidentSerializer
from flask import current_app
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


class ServiceData():

    def __init__(self,session):
        self.session = session
        self.api_client = ApiClient()

    def count_all(self):
        with self.session() as s:
            result = s.query(Service).count()
            return result
        
    def get_service_name(self, id_service):
        with self.session() as s:
            result = s.query(Service).filter(Service.id_service == id_service).first()
            return result.name

    def get_all(self):

        with self.session() as s:
            result = s.query(Service).all()
            pydantic_result = [ServiceSerializer.from_orm(item) for item in result]
            return [item.dict() for item in pydantic_result]
        
    def count_all_and_group_by_incident(self):
        with self.session() as s:
            incidents = self.api_client.get_incidents()

            if not incidents:
                return []

            for item in incidents:
                item["service"] = self.get_service_name(item["service"])

            return [ServiceGroupByIncidentSerializer(
                name=item["service"],
                count=item["count"]).dict() for item in incidents]