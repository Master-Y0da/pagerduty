from flask import Blueprint
from flask_restx import Api


from .services.service import ns as services
from .incidents.incidents import ns as incidents

v1 = Blueprint('v1', __name__)
api = Api(v1, version='1.0', title='API v1', description='API v1', doc='/docs')

api.add_namespace(services)
api.add_namespace(incidents)




