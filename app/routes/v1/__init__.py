from flask import Blueprint
from flask_restx import Api


from .services.service import ns as services
from .incidents.incidents import ns as incidents
from .teams.teams import ns as teams
from .escalation_policies.escalation_policies import ns as escalation_policies

v1 = Blueprint('v1', __name__)
api = Api(v1, version='1.0', title='API v1', description='API pagerduty', doc='/docs')

api.add_namespace(services)
api.add_namespace(incidents)
api.add_namespace(teams)
api.add_namespace(escalation_policies)
