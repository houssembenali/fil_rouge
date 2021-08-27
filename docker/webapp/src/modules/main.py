from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')
# main = Flask(__name__, template_folder='modules')

@main.route('/')
def index():
    return render_template('index.html')


@main.errorhandler(404)
def not_found(e):
    """Page not found."""
    return render_template("404.html")
# from modules import db, create_app
# db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.