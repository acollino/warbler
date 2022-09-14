from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, URLField, EmailField

# Changed DataRequired to InputRequired per wtforms documentation recommendations
from wtforms.validators import InputRequired, Email, Length, Optional


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[InputRequired()])
    email = EmailField("E-mail", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    image_url = URLField("(Optional) Profile Image URL", validators=[Optional()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class EditProfileForm(FlaskForm):
    """Form for a user to update their profile details."""

    username = StringField("Username", validators=[Optional()])
    email = EmailField("E-mail", validators=[Optional(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    image_url = URLField("Profile Image URL", validators=[Optional()])
    header_image_url = URLField("Header Image URL", validators=[Optional()])
    bio = TextAreaField("Bio", validators=[Optional()])
