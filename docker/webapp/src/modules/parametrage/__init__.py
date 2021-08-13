"""
The parametrage Blueprint handles the creation, modification.
"""
from flask import Blueprint
parametrage_blueprint = Blueprint('parametrage', __name__, template_folder='templates')

from . import routes
