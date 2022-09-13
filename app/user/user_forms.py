from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

# Changed DataRequired to InputRequired per wtforms documentation recommendations
from wtforms.validators import InputRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[InputRequired()])
    email = StringField("E-mail", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    image_url = StringField("(Optional) Image URL")


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])
