from flask import Blueprint, current_app
from flask_restx import Namespace, Resource
from .data.team_data import TeamData


ns = Namespace('teams', description='Teams')


@ns.route('/')
class Teams(Resource):

    def __init__(self, *args, **kwargs):
        super(Teams, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["incidents"]
        self.data_instance = TeamData(self.session)

    
    @ns.response(200, 'Incidents')
    def get(self):
        return self.data_instance.get_all_groupe_by_service()



