from flask import Blueprint, current_app
from flask_restx import Namespace, Resource
from .data.team_data import TeamData


ns = Namespace('teams', description='Teams')


class TeamsResource(Resource):

    def __init__(self, *args, **kwargs):
        super(TeamsResource, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["teams"]
        self.data_instance = TeamData(self.session)

@ns.route('/by-service-status')
class Teams(TeamsResource):

    @ns.response(200, 'Incidents')
    def get(self):
        return self.data_instance.number_of_teams_and_related_services()


@ns.route('/by-service-status/csv-report')
class CsvReport(TeamsResource):
    def get(self):
        return self.data_instance.get_csv_report()
