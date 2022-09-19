from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path, environ
from dotenv import load_dotenv

# Create instance of the database
db = SQLAlchemy()
bcrypt = Bcrypt()

# The argument refers to which .env file to use, ie test.env, dev.env
# The default of .env is used for production on Heroku
def init_app(envFile=".env"):
    """Initialize the application"""

    # Load environ vars from the given file, which includes a var for the given config name
    base_directory = path.abspath(f"{path.dirname(__file__)}/..")
    load_dotenv(path.join(base_directory, envFile))
    # Load_dotenv is used here, rather than in the config file, because using it in config
    # causes the environment vars to be set as soon as the file is imported or accessed in
    # config.from_object("config.DevConfig"). The load_dotenv function executes each time it
    # occurs in the config file, including in different config classes - leading to development
    # or production values occuring unexpectedly in the testing configuration.

    # Initialize the app and set the required configs
    app = Flask(__name__)
    app.config.from_object(environ.get("CONFIG"))

    # Initialize database
    db.init_app(app)

    """ 
    Use app_context to ensure functions within the block can access current_app, which
    can be helpful to access the config or log errors.
    """
    with app.app_context():
        from app.user import user_bp
        from app.message import message_bp
        from app.home import home_bp

        # Register blueprints. If needed, url_prefix param can be set to append a string (ie '/users') to the route url.
        app.register_blueprint(user_bp)
        app.register_blueprint(message_bp)
        app.register_blueprint(home_bp)

        return app
