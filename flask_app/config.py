# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Bailey Roberts


"""Flask config class."""
from datetime import timedelta
from pathlib import Path


class Config(object):
    """ Sets the Flask base configuration that is common to all environments. """
    DEBUG = False
    SECRET_KEY = 'qkd569wdffiuDobNoLLPQ'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = Path(__file__).parent.parent.joinpath("data")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('Database.db'))
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static/img")


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    # Echo SQL to the console, useful for debugging database queries
    SQLALCHEMY_ECHO = True
    # Allow forms to be submitted from the tests without the CSRF token
    WTF_CSRF_ENABLED = False
    # DEBUG = True
