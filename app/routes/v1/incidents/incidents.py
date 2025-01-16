from flask import Blueprint, current_app
from flask_restx import Namespace, Resource
from .data.incident_data import IncidentData


ns = Namespace('incidents', description='Incidents')

class IncidentResource(Resource):
    def __init__(self, *args, **kwargs):
        super(IncidentResource, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["incidents"]
        self.data_instance = IncidentData(self.session)

@ns.route('/')
class Incidents(IncidentResource):

    @ns.response(200, 'Incidents')
    def get(self):
        return self.data_instance.get_all_groupe_by_service()


@ns.route('/by-service-status')
class IncidentsByServiceStatus(IncidentResource):

    @ns.response(200, 'Incidents by Service and Status')
    def get(self):
        return self.data_instance.get_all_groupe_by_service_and_status()


@ns.route('/by-service-status/csv-report')
class CsvReport(IncidentResource):

    @ns.response(200, 'success', headers={'Content-Disposition': 'attachment; filename=report.csv'})
    def get(self):
        return self.data_instance.get_csv_report()


@ns.route('/top-incidents')
class TopIncidents(IncidentResource):

    @ns.response(200, 'success')
    def get(self):
        return self.data_instance.get_top_incidents_by_service()


@ns.route('/top-incidents/graph')
class TopIncidentsGraph(IncidentResource):

    @ns.response(200, 'success')
    def get(self):
        return self.data_instance.get_top_incidents_graph()
