"""Classes for Flask configurations."""
from os import environ, path
from dotenv import load_dotenv

# Get the path to the directory of this file
base_directory = path.abspath(path.dirname(__file__))
# The .env file found in that same directory will be loaded


class Config:
    """Set the base configuration for Flask."""

    load_dotenv(path.join(base_directory, ".env"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SECRET_KEY = environ.get("SECRET_KEY")


class DevConfig(Config):
    """Set the development configuration for Flask."""

    SQLALCHEMY_ECHO = True
    DEBUG = True


class ProdConfig(Config):
    """Set the production configuration for Flask."""

    SQLALCHEMY_ECHO = False
    DEBUG = False


class TestConfig:
    """Set the testing configuration for Flask."""

    load_dotenv(path.join(base_directory, "test.env"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_ECHO = True
    DEBUG = True
    TESTING = True
    # Per Springboard, don't have WTForms use CSRF at all, since it's a pain to test
    WTF_CSRF_ENABLED = False
