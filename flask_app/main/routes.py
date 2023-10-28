# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi

from flask import Blueprint, render_template, url_for
from flask_login import current_user
from flask_app.models import Profile, User
from flask_app import photos

main_bp = Blueprint('main', __name__)


@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    if not current_user.is_anonymous:
        name = current_user.firstname
        profile = Profile.query.join(User).filter_by(id=current_user.id).first()
        if profile:
            if profile.photo != None:
                url = photos.url(
                    profile.photo)  # uses the global photos plus the photo file name to determine the full url path
            else:
                url = url_for('static', filename='Default_Account_Image.png')
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = None
    return render_template('Main_index.html', title='Home page', name=name, url=url)


@main_bp.route('/about')
def about():
    if not current_user.is_anonymous:
        profile = Profile.query.join(User).filter_by(id=current_user.id).first()
        if profile:
            if profile.photo != None:
                url = photos.url(
                    profile.photo)  # uses the global photos plus the photo file name to determine the full url path
            else:
                url = url_for('static', filename='Default_Account_Image.png')
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = None
    return render_template('About_index.html', url=url)
