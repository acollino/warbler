"""Classes for Flask configurations."""
from os import environ


class Config:
    """Set the base configuration for Flask."""

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


class TestConfig(Config):
    """Set the testing configuration for Flask."""

    SQLALCHEMY_ECHO = True
    DEBUG = True
    TESTING = True
    # Per Springboard, don't have WTForms use CSRF at all, since it's difficult to test
    WTF_CSRF_ENABLED = False
