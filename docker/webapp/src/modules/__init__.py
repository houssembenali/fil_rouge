from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate # Was missing in example code.

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    initialize_extensions(app)


    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # from .models import User

    # @login_manager.user_loader
    # def load_user(user_id):
    #     # since the user_id is just the primary key of our user table, use it in the query for the user
    #     return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from modules.login.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for projects
    from modules.projects.routes import projects_blueprint
    app.register_blueprint(projects_blueprint)

    from modules.addproject.routes import addproject_blueprint
    app.register_blueprint(addproject_blueprint)

    from modules.parametrage.routes import parametrage_blueprint
    app.register_blueprint(parametrage_blueprint)
    
    return app

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    migrate = Migrate(app, db) # Was missing in example code.
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Flask-Login configuration
    from modules.login.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # @login.user_loader
    # def load_user(user_id):
    #     return User.query.filter(User.id == int(user_id)).first()