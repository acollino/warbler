from flask import session, g
from . import user_bp
from app.models import User

CURR_USER_KEY = "curr_user"

# changed from before_request to ensure it occurs even for other blueprints
@user_bp.before_app_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
