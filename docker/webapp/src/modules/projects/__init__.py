"""
The projects Blueprint handles.
"""
from flask import Blueprint
projects_blueprint = Blueprint('projects', __name__, template_folder='templates')

from . import routes
