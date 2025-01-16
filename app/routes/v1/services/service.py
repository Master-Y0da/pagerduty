from wsgiref import headers
from flask import Blueprint, current_app
from flask_restx import Namespace, Resource
from .data.service_data import ServiceData


ns = Namespace('services', description='Services')


class ServicesResource(Resource):

    def __init__(self, *args, **kwargs):
        super(ServicesResource, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["services"]
        self.data_instance = ServiceData(self.session)


@ns.route('/')
class Services(ServicesResource):

    @ns.response(200, 'Services')
    def get(self):
        return self.data_instance.get_all()


@ns.route('/count')
class ServicesCount(ServicesResource):
    @ns.response(200, 'success')
    def get(self):
        total = self.data_instance.count_all()
        return {"number_of_services": total}


@ns.route('/incident-count')
class IncidentCount(ServicesResource):

    @ns.response(200, 'success')
    def get(self):
        return self.data_instance.count_all_and_group_by_incident()


@ns.route('/count/csv-report')
class CsvReportCount(ServicesResource):

    @ns.response(200, 'success', headers={'Content-Disposition': 'attachment; filename=report.csv'})
    def get(self):
        return self.data_instance.get_csv_report('count')


@ns.route('/incident-count/csv-report')
class CsvReport(ServicesResource):

    @ns.response(200, 'success', headers={'Content-Disposition': 'attachment; filename=report.csv'})
    def get(self):
        return self.data_instance.get_csv_report('incident-count')
