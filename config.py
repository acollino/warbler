"""Classes for Flask configurations."""
from os import environ, path
from dotenv import load_dotenv

# Get the path to the directory of this file
base_directory = path.abspath(path.dirname(__file__))

# Load the .env file found in the same directory
load_dotenv(path.join(base_directory, ".env"))


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
