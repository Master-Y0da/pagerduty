from flask import Blueprint, current_app
from flask_restx import Namespace, Resource
from .data.ep_data import EpData


ns = Namespace('escalation_policies', description='Escalation Policies')


class EpResource(Resource):

    def __init__(self, *args, **kwargs):
        super(EpResource, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["services"]
        self.data_instance = EpData(self.session)

@ns.route('/count')
class EscalationPolicies(EpResource):

    @ns.response(200, 'Services')
    def get(self):
        return self.data_instance.number_of_ep_and_services_teams()


@ns.route('/count/csv-report')
class CsvReport(EpResource):

    @ns.response(200, 'success', headers={'Content-Disposition': 'attachment; filename=report.csv'})
    def get(self):
        return self.data_instance.get_csv_report()
