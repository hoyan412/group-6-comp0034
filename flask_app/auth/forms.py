# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Rayan Souissi - Aydan Guliyeva - Ho Yan Or


from flask_wtf import FlaskForm,validators
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_app import photos
from flask_app.models import User, Profile

class SignupForm(FlaskForm):
    first_name = StringField(label='First name*:', validators=[DataRequired()])
    last_name = StringField(label='Last name*:', validators=[DataRequired()])
    dob = DateField(label='Date of birth*:', validators=[DataRequired()])
    email = EmailField(label='Email address*:', validators=[DataRequired()])
    password = PasswordField(label='Password*:', validators=[DataRequired()])
    password_confirm = PasswordField(label='Confirm Password*:',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address.')

class LoginForm(FlaskForm):
    email = EmailField(label='Email address:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is None:
            raise ValidationError('There is no account registered with this email address, please create an account')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password.')

