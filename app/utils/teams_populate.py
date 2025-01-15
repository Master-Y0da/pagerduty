import httpx,os
from flask import current_app
from app.routes.v1.teams.models.team_model import Teams


def save_teams(teams):

    session = current_app.db_session["teams"]
    with session() as s:
        with s.begin():
            for item in teams["teams"]:
                result = Teams(name=item["name"], id_team=item["id"], description=item["description"],
                                summary=item["summary"], type=item["type"])
                s.add(result)
        s.commit()


async def get_teams():
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.get(os.getenv('PAGERDUTY_API_TEAMS'), 
                        headers={"Authorization": f"Token token={os.getenv('PAGERDUTY_API_KEY')}"})
        except httpx.HTTPStatusError as e:
            print(e)
            raise e
        except httpx.RequestError as e:
            print(e)
            raise e
        
        save_teams(response.json())

        return response.json()