import httpx,os
from flask import current_app
from app.routes.v1.escalation_policies.models.escalation_policies_model import EscalationPolicies


def save_ep(teams):

    session = current_app.db_session["escalation_policies"]
    with session() as s:
        with s.begin():
            for item in teams["escalation_policies"]:
                result = EscalationPolicies(
                    name=item["name"],
                    id_ep=item["id"],
                    summary=item["summary"],
                    type=item["type"],
                    teams=item["teams"],
                    services=item["services"]
                )
                s.add(result)
        s.commit()


async def get_ep():
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.get(os.getenv('PAGERDUTY_API_EP'),
                        headers={"Authorization": f"Token token={os.getenv('PAGERDUTY_API_KEY')}"})
        except httpx.HTTPStatusError as e:
            print(e)
            raise e
        except httpx.RequestError as e:
            print(e)
            raise e

        save_ep(response.json())

        return response.json()
