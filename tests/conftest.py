# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Bailey Roberts - Youssef Alaoui

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import multiprocessing

from flask import url_for

from flask_app import create_app
from flask_app import db as _db
from flask_app.config import TestingConfig



@pytest.fixture(scope='session')
def app(request):
    """ Returns a session wide Flask app """
    _app = create_app(TestingConfig)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    """ Exposes the Werkzeug test client for use in the tests. """
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """
    Returns a session wide database using a Flask-SQLAlchemy database connection.
    """
    _db.app = app
    _db.create_all()

    yield _db
    #_db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """ Rolls back database changes at the end of each test """
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)
    db.session = session_
    yield session_
    transaction.rollback()
    connection.close()
    session_.remove()


@pytest.fixture(scope='function')
def user(db):
    """ Creates a user without a profile. """
    from flask_app.models import User
    from datetime import datetime
    user = User(firstname='FN_test', lastname='LN_test', dob= datetime.now(),
                email='fn.ln@test.com', password='password')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='function')
def profile(db, user):
    """ Creates a user profile without a """
    from flask_app.models import Profile
    profile = Profile(username='fn_ln',  bio='bio of fn_ln', photo='Default_Account_Image.png', gender="Male", user_id = user.id)
    db.session.add(profile)
    db.session.commit()
    return profile

@pytest.fixture(scope='class')
def chrome_driver(request):
    """ Fixture for selenium webdriver with options to support running in GitHub actions"""
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--headless")
   # options.add_argument("--window-size=1920,1080")
    chrome_driver = webdriver.Chrome(options=options)
    request.cls.driver = chrome_driver
    chrome_driver.maximize_window()
    yield
    chrome_driver.close()

@pytest.fixture(scope='class')
def selenium(app):
    """
    Fixture to run the Flask app
    A better alternative would be to use flask-testing live_server
    """
    process = multiprocessing.get_context('fork').Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()

