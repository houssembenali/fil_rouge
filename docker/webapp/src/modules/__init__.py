from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate # Was missing in example code.


#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = "users.login"


######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app


##########################
#### Helper Functions ####
##########################

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    migrate = Migrate(app, db) # Was missing in example code.
    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)

    # Flask-Login configuration
    from modules.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from modules.recipes import recipes_blueprint
    from modules.users import users_blueprint
    from modules.parametrage import parametrage_blueprint
    from modules.projects import projects_blueprint
    from modules.addproject import addproject_blueprint
    

    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(parametrage_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(addproject_blueprint)
