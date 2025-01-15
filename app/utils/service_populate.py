import httpx,os
from flask import current_app
from app.routes.v1.services.models import Service


def save_services(services):

    session = current_app.db_session["services"]
    with session() as s:
        with s.begin():
            for item in services["services"]:
                result = Service(name=item["name"], id_service=item["id"], description=item["description"], status=item["status"])
                s.add(result)
        s.commit()


async def get_services():
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.get(os.getenv('PAGERDUTY_API_SERVICES'), 
                        headers={"Authorization": f"Token token={os.getenv('PAGERDUTY_API_KEY')}"})
        except httpx.HTTPStatusError as e:
            print(e)
            raise e
        except httpx.RequestError as e:
            print(e)
            raise e
        
        save_services(response.json())

        return response.json()