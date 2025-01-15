from flask import Blueprint, current_app
from flask_restx import Namespace, Resource
from .data.incident_data import IncidentData


ns = Namespace('incidents', description='Incidents')


@ns.route('/')
class Incidents(Resource):

    def __init__(self, *args, **kwargs):
        super(Incidents, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["incidents"]
        self.data_instance = IncidentData(self.session)

    
    @ns.response(200, 'Incidents')
    def get(self):
        return self.data_instance.get_all_groupe_by_service()


@ns.route('/by-service-status')
class IncidentsByServiceStatus(Resource):

    def __init__(self, *args, **kwargs):
        super(IncidentsByServiceStatus, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["incidents"]
        self.data_instance = IncidentData(self.session)

    
    @ns.response(200, 'Incidents by Service and Status')
    def get(self):
        return self.data_instance.get_all_groupe_by_service_and_status()


