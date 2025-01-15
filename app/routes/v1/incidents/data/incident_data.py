
from ..models import Incident
from ..serializers.IncidentSerializer import IncidentSerializer, IncidentsGroupByServiceSerializer, IncidentsGroupByServiceAndStatusSerializer
from flask import current_app
from sqlalchemy import func
from itertools import groupby
from operator import itemgetter


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
