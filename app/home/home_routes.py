from flask import render_template, g
from . import home_bp
from app.models import Message


@home_bp.route("/")
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    if g.get("user", None):
        following_ids = [user.id for user in g.user.following]
        messages = (
            Message.query.filter(
                (Message.user_id.in_(following_ids)) | (Message.user_id == g.user.id)
            )
            .order_by(Message.timestamp.desc())
            .limit(100)
            .all()
        )
        liked_msg_ids = [message.id for message in g.user.likes]
        return render_template("home/home.html", messages=messages, likes=liked_msg_ids)

    else:
        return render_template("home/home-anon.html")


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

# Changed to after_app_request from after_request to occur after requests from other blueprints
@home_bp.after_app_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers[
        "Cache-Control"
    ] = "no-cache, no-store, must-revalidate, public, max-age=0"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    return req
