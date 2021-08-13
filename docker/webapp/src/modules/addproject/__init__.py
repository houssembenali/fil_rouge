"""
The addproject Blueprint handles.
"""
from flask import Blueprint
addproject_blueprint = Blueprint('addproject', __name__, template_folder='templates')

from . import routes
