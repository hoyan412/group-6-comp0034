
# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Bailey Roberts -

from flask_wtf import FlaskForm, validators, form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_login import login_required, current_user
from flask_app import photos
from flask_app.models import User, Profile




class PostForm(FlaskForm):
    post_title = TextAreaField('Title (Required)', validators=[DataRequired(message='Title is required')])
    post = TextAreaField('Post (Required)', validators=[DataRequired(message='Post is required')])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')
