from flask import Blueprint

user_bp = Blueprint("user", __name__, template_folder="templates")

# These imports occur after blueprint creation to avoid circular imports
from . import user_routes
