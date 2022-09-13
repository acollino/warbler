from flask import Blueprint

message_bp = Blueprint("message", __name__, template_folder="templates")

# These imports occur after blueprint creation to avoid circular imports
from . import message_routes
