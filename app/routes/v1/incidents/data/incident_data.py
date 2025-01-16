
from ..models import Incident
from ..serializers.IncidentSerializer import IncidentSerializer, IncidentsGroupByServiceSerializer, IncidentsGroupByServiceAndStatusSerializer
from flask import current_app, Response
from sqlalchemy import func
from itertools import groupby
from operator import itemgetter
from pandas import DataFrame as df
import matplotlib.pyplot as plt
import io


class IncidentData():

    def __init__(self,session):
        self.session = session

    def get_all(self):
        with self.session() as s:
            result = s.query(Incident).all()
            pydantic_result = [IncidentSerializer.from_orm(item) for item in result]
            return [item.dict() for item in pydantic_result]

    def get_all_groupe_by_service(self):
        with self.session() as s:
            query = s.query(Incident.id_incident,Incident.service,func.count('*').label('count')
            ).group_by(
                Incident.id_incident,
                Incident.service
            )

            result = query.all()

            if not result:
                return []

            sorted_result = sorted(result, key=itemgetter(1, 2))
            clean = [next(v) for _, v in groupby(sorted_result, key=itemgetter(1, 2))]

            return [IncidentsGroupByServiceSerializer(
                service=item.service,
                count=item.count).dict() for item in clean]


    def get_all_groupe_by_service_and_status(self):
        with self.session() as s:
            query = s.query(Incident.id_incident,Incident.service,Incident.status,func.count('*').label('count')
            ).group_by(
                Incident.id_incident,
                Incident.service,
                Incident.status
            )

            result = query.all()

            if not result:
                return []

            sorted_result = sorted(result, key=itemgetter(1, 2))
            clean = [next(v) for _, v in groupby(sorted_result, key=itemgetter(1, 2))]

            return [IncidentsGroupByServiceAndStatusSerializer(
                incident=item.id_incident,
                service=item.service,
                status=item.status,
                count=item.count).dict() for item in clean]


    def get_csv_report(self):

        data = self.get_all_groupe_by_service_and_status()

        csv = df(data)

        return Response(
            csv.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=services.csv"})

    def get_top_incidents_by_service(self):
        with self.session() as s:
            query = s.query(Incident.service,func.count(Incident.id).label('count')
            ).group_by(
                Incident.service,
            ).order_by(
                func.count('*').desc()
            )

            result = query.all()

            if not result:
                return []

            top_service = result[0]

            query = s.query(Incident.status,func.count(Incident.id).label('count')
            ).group_by(
                Incident.status
            ).filter(Incident.service == top_service.service
            )

            return {
                "service": top_service.service,
                "total": top_service.count,
                "incidents_status": {item.status: item.count for item in query.all()}
            }

    def get_top_incidents_graph(self):

        data = self.get_top_incidents_by_service()

        x = [data["service"]]

        statuses = list(data["incidents_status"].keys())
        counts = list(data["incidents_status"].values())

        plt.figure(figsize=(8, 5))
        bars = plt.bar(statuses, counts, color=['orange', 'green', 'red'])

        for bar in bars:
            plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(bar.get_height()),
            ha='center',
            va='bottom',
            fontsize=10
        )

        plt.title(f"Incident Status for Service {x}", fontsize=14)
        plt.xlabel("Incident Status", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return Response(buffer, mimetype='image/png')
