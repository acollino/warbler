from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create instance of the database
db = SQLAlchemy()
bcrypt = Bcrypt()

# Use the development configuration by default, change to ProdConfig before deploying
def init_app(configStr="config.DevConfig"):
    """Initialize the application"""

    app = Flask(__name__)
    app.config.from_object(configStr)

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
