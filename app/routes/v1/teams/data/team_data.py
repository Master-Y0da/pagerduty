
from ..models.team_model import Teams
from ..serializers.team_serializer import TeamSerializer
from flask import current_app, Response
from sqlalchemy import func
from typing import Dict, Any
import asyncio, httpx
from pandas import DataFrame as df


class ApiClient:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url

    async def _get_services(self) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}/api/v1/services/")
            response.raise_for_status()
            return response.json()

    def get_services(self) -> Dict[str, Any]:
        try:
            return asyncio.run(self._get_services())
        except Exception as e:
            current_app.logger.error(f"Error fetching services: {str(e)}")
            return {"error": str(e)}


class TeamData():

    def __init__(self,session):
        self.session = session
        self.api_client = ApiClient()

    def get_all(self):
        with self.session() as s:
            services = self.api_client.get_services()
            current_app.logger.info(f"Services: {services}")
            result = s.query(Teams).all()
            pydantic_result = [TeamSerializer.from_orm(item) for item in result]
            return [item.dict() for item in pydantic_result]

    def number_of_teams_and_related_services(self):
        with self.session() as s:
            services = self.api_client.get_services()
            teams = s.query(Teams).all()

            if not services:
                return {"error": "No services found"}

            if not teams:
                return {"error": "No teams found"}

            results = {
                "number_of_teams": s.query(Teams).count(),
                "teams": []
            }

            for item in services:
                current_app.logger.info(f"Item: {item}")
                if item["team"]:
                   for service_team in item["team"]:
                        matching_team = next((team for team in teams if team.id_team == service_team["id"]), None)
                        if matching_team:
                            results["teams"].append(
                                {
                                    "team": matching_team.name,
                                    "service": item["name"]
                                })
            return results

    def get_csv_report(self):
        data = self.number_of_teams_and_related_services()

        transformed_data = []

        transformed_data.append({
            'number_of_teams': data['number_of_teams'],
            'team': '',
            'service': ''
        })

        for team_service in data['teams']:
            transformed_data.append({
                'number_of_teams': data['number_of_teams'],
                'team': team_service['team'],
                'service': team_service['service']
            })

        data = transformed_data

        csv = df(data)

        return Response(
            csv.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition":
                        "attachment; filename=services.csv"})
