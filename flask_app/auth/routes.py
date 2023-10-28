
# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Ho Yan Or

from sqlite3 import IntegrityError

from flask import Blueprint, render_template, flash, redirect, url_for
from urllib.parse import urlparse, urljoin
from flask import request
from flask_app import db, login_manager
from flask_app.auth.forms import SignupForm, LoginForm
from flask_app.models import User
from datetime import timedelta, datetime
from flask import abort
from flask import make_response
from flask_login import login_user, login_required, logout_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(firstname=form.first_name.data,
                    lastname=form.last_name.data,
                    dob=form.dob.data,
                    email=form.email.data)
        if user.dob>=datetime.date(datetime.now()):
            flash(f"Date of Birth must be in the past", "danger")
            return render_template('Auth_signup.html', title='Sign Up', form=form)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.firstname}. You have successfully registered.","success")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. Please try again ', "error")
            return redirect(url_for('auth.signup'))

        response = make_response(redirect(url_for('auth.login')))
        response.set_cookie("name", user.firstname)
        return response

    return render_template('Auth_signup.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.index', name='user.firstname'))
    return render_template('Auth_login.html', title='Login', form=form, url = url_for('static', filename='Default_Account_Image.png'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@login_manager.user_loader
def load_user(user_id):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        return User.query.get(user_id)
    return None


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.','warning')
    return redirect(url_for('auth.login'))
