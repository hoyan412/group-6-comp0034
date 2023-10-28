
# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Bailey Roberts

from flask import render_template, Blueprint, url_for
from flask_login import current_user, login_required

from flask_app import photos
from flask_app.models import User, Profile

dash_html_bp = Blueprint('dash_html', __name__, url_prefix='/dash_html')


@dash_html_bp.route('/')
def index():
    if not current_user.is_anonymous:
        current_profile = Profile.query.join(User).filter_by(id=current_user.id).first()

        if current_profile:
            if current_profile.photo != None:
                url = photos.url(current_profile.photo)  # uses the global photos plus the photo file name to determine the full url path
            else:
                url = url_for('static', filename='Default_Account_Image.png')
        else:
            url = url_for('static', filename='Default_Account_Image.png')
    else:
        url = None

    return render_template('Dasha_app.html', title="dash_html", url=url)
