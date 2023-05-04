""" API """
from flask import Blueprint
from flask_restx import Api

from .user import api as user_ns
from .connection_request import api as connection_request_ns
from .task import api as task_ns
from .connection import api as connection_ns
from .filter import api as filter_ns

import socket

authorizations = {
    'Access Token': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization',
    'description': 'For the value, input "Bearer \<Access Token\>" Just like in Postman.'
    }
}
blueprint = Blueprint('api', __name__)
api = Api(blueprint, title='Task Management API', version='1.0', 
          description='API for task management.', default_swagger_filename='task_api.json',
          security='Access Token', authorizations=authorizations)
api.add_namespace(user_ns)
api.add_namespace(connection_ns)
api.add_namespace(connection_request_ns)
api.add_namespace(task_ns)
api.add_namespace(filter_ns)