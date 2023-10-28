# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Aydan Guliyeva

from flask_wtf import FlaskForm, validators, form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, RadioField
from wtforms.fields.html5 import EmailField, DateField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_login import login_required, current_user
from flask_app import photos
from flask_app.models import User, Profile


class ProfileForm(FlaskForm):
    username = StringField(label='Username (Required):', validators=[DataRequired(message='Username is required')])
    bio = TextAreaField(label='Bio:', description='Write something about yourself')
    photo = FileField('Profile Picture:', validators=[FileAllowed(photos, 'Images only')])
    gender = RadioField('Gender (Required):',
                        choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')],
                        validators=[DataRequired(message='Gender is required')])
    age = IntegerField('Age:')

    def validate_username(self, username):
        account = Profile.query.filter_by(username=username.data).first()
        account_check = Profile.query.join(User).filter_by(id=current_user.id).first()
        if account is not None and account != account_check:
            raise ValidationError('Username already exists, please choose another username')


class EditProfileForm(FlaskForm):
    firstname = StringField(label='First name')
    lastname = StringField(label='Last name')
    email = EmailField(label='Email address')
    dob = DateField(label='Date of birth')


class PasswordForm(FlaskForm):
    new_password = PasswordField('Password:', validators=[DataRequired()])
    new_password_confirm = PasswordField(label='Confirm Password:',
                                         validators=[DataRequired(),
                                                     EqualTo('new_password', message='Passwords must match')])


class EmailForm(FlaskForm):
    email = EmailField('Email address:', validators=[DataRequired()])


class FirstNameForm(FlaskForm):
    firstname = StringField(label='First name:', validators=[DataRequired()])


class LastNameForm(FlaskForm):
    lastname = StringField(label='Last name:', validators=[DataRequired()])


class DateOfBirthForm(FlaskForm):
    dob = DateField(label='Date of birth:')
