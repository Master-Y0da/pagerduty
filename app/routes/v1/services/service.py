from flask import Blueprint, current_app
from flask_restx import Namespace, Resource
from .data.service_data import ServiceData


ns = Namespace('services', description='Services')


@ns.route('/')
class Services(Resource):

    def __init__(self, *args, **kwargs):
        super(Services, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["services"]
        self.data_instance = ServiceData(self.session)

    
    @ns.response(200, 'Services')
    def get(self):
        return self.data_instance.get_all()
        
    
@ns.route('/count')
class ServicesCount(Resource):

    def __init__(self, *args, **kwargs):
        super(ServicesCount, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["services"]
        self.data_instance = ServiceData(self.session)

    
    @ns.response(200, 'Services Count')
    def get(self):
        total = self.data_instance.count_all()
        return {"number_of_services": total}


@ns.route('/incident-count')
class IncidentCount(Resource):

    def __init__(self, *args, **kwargs):
        super(IncidentCount, self).__init__(*args, **kwargs)
        self.session = current_app.db_session["incidents"]
        self.data_instance = ServiceData(self.session)

    
    @ns.response(200, 'Incidents Count')
    def get(self):
        return self.data_instance.count_all_and_group_by_incident()


