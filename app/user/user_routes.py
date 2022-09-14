from crypt import methods
from flask import render_template, redirect, flash, request, g, current_app
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .user_forms import UserAddForm, LoginForm, EditProfileForm
from app.models import User, Message
from .user_util import do_login, do_logout
from app import db
from . import user_bp


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("user/signup.html", form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template("user/signup.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("user/login.html", form=form)


@user_bp.route("/logout")
def logout():
    """Handle logout of user."""
    do_logout()
    return redirect("/")


@user_bp.route("/users")
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get("q")

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template("user/index.html", users=users)


@user_bp.route("/users/<int:user_id>")
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    # snagging messages in order from the database;
    # user.messages won't be in order by default
    messages = (
        Message.query.filter(Message.user_id == user_id)
        .order_by(Message.timestamp.desc())
        .limit(100)
        .all()
    )
    return render_template("user/show.html", user=user, messages=messages)


@user_bp.route("/users/<int:user_id>/following")
def show_following(user_id):
    """Show list of people this user is following."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template("user/following.html", user=user)


@user_bp.route("/users/<int:user_id>/followers")
def users_followers(user_id):
    """Show list of followers of this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    return render_template("user/followers.html", user=user)


@user_bp.route("/users/follow/<int:follow_id>", methods=["POST"])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@user_bp.route("/users/stop-following/<int:follow_id>", methods=["POST"])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")


@user_bp.route("/users/profile", methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.authenticate(g.user.username, form.password.data)

        if user:
            for field, value in form.data.items():
                valid_field = field != "csrf_token" and field != "password"
                not_empty = value != ""
                if valid_field and not_empty:
                    setattr(user, field, value)
            try:
                db.session.commit()
                g.user = user
                return redirect(f"/users/{user.id}")
            except SQLAlchemyError as e:
                current_app.log_exception(e)
                db.session.rollback()
                flash("Due to an error, your profile could not be updated.", "danger")

    return render_template("user/edit.html", form=form)


@user_bp.route("/users/delete", methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


@user_bp.route("/users/add_like/<int:msg_id>", methods=["POST"])
def add_like(msg_id):
    """Toggle a like from the current user to a message."""

    if not g.user:
        flash("You must be logged in to like a message.", "danger")
        return redirect("/")

    msg = Message.query.get_or_404(msg_id)
    if msg in g.user.likes:
        g.user.likes.remove(msg)
    else:
        g.user.likes.append(msg)
    db.session.commit()

    # refresh the current requesting page, whether it's the home page or message details
    return redirect(request.referrer)


@user_bp.route("/users/<int:user_id>/likes", methods=["GET"])
def show_likes(user_id):
    """Display the messages that a user has liked."""

    user = User.query.get_or_404(user_id)
    messages = user.likes

    return render_template("user/likes.html", user=user, messages=messages)
