from ..models.escalation_policies_model import EscalationPolicies
from ..serializers.ep_serializer import EpCountSerializer ,EscalationPolicySerializer
from flask import current_app, Response
from sqlalchemy import func
from typing import Dict, Any
import asyncio, httpx
import pandas as pd
from pandas import DataFrame as df


class EpData():

    def __init__(self,session):
        self.session = session

    def number_of_ep_and_services_teams(self):
        with self.session() as s:
            ep = s.query(EscalationPolicies).all()

            if not ep:
                return []

            result = EpCountSerializer(
                count=s.query(EscalationPolicies).count(),
                ep=[EscalationPolicySerializer.from_orm(item) for item in ep]
            )

            return result.dict()


    def get_csv_report(self):
        data = self.number_of_ep_and_services_teams()

        df1 = [{'count': data["count"]}]

        for item in data["ep"]:
            for t in item["teams"]:
                df1.append({'escalation_policy': item["id_ep"], 'team': t["id"]})
            for s in item["services"]:
                df1.append({'escalation_policy': item["id_ep"], 'service': s["id"]})

        csv = df(df1)

        return Response(
            csv.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition":
                        "attachment; filename=services.csv"})
