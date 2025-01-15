import httpx,os
from flask import current_app
from app.routes.v1.incidents.models import Incident


def save_incidents(services):
    current_app.logger.info(services)
    session = current_app.db_session["incidents"]
    with session() as s:
        with s.begin():
            for item in services["incidents"]:
                result = Incident(id_incident=item["id"], service=item["service"]["id"], summary=item["summary"], status=item["status"])
                s.add(result)
        s.commit()


async def get_incidents():
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.get(os.getenv('PAGERDUTY_API_INCIDENTS'), 
                        params={"total": True,"date_range": "all"},
                        headers={"Authorization": f"Token token={os.getenv('PAGERDUTY_API_KEY')}"})
            current_app.logger.info(response.json())
        except httpx.HTTPStatusError as e:
            print(e)
            raise e
        except httpx.RequestError as e:
            print(e)
            raise e
        
        save_incidents(response.json())

        return