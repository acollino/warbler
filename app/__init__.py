from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create instance of the database
db = SQLAlchemy()
bcrypt = Bcrypt()

# name this create_app() instead?
def init_app():
    """Initialize the application"""

    app = Flask(__name__)
    # Use the development configuration, change to ProdConfig before deploying
    app.config.from_object("config.DevConfig")
    # Can also use the config string as an argument, pass it in when init is called

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
