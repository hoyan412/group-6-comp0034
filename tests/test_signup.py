# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Authors: Rayan Souissi

from flask_app.models import User

class TestSignUp:

    def test_signup_succeeds(self, client):
        """
        GIVEN A user is not registered
        WHEN they submit a valid registration form
        THEN they  should be redirected to the login page with an account created message and there should be a
        record in the user table in the database
        """

        count = User.query.count()
        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                        email='signup_test@test.com', password='password2', password_confirm='password2'),
                                        follow_redirects=True)
        count2 = User.query.count()
        assert count2 - count == 1      #new user correctly saved in the database
        assert response.status_code == 200
        assert b'Hello, FN_test. You have successfully registered.' in response.data


    def test_signup_already_used_email(self, client):
        """
        GIVEN A user is not registred
        WHEN they submit a registration form with an already used email address
        THEN the page should be reloaded and there shouldn't be a record in user table in the database and a warning
        message should appear
        """

        count = User.query.count()
        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                        email='test@test.test', password='password2', password_confirm='password2'),
                                        follow_redirects=True)

        response1 = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                        email='test@test.test', password='password2', password_confirm='password2'),
                                        follow_redirects=True)
        count2 = User.query.count()
        assert count2 - count == 1  #First user correctly saved in the database but not the second one
        assert response.status_code == 200
        assert response1.status_code == 200
        assert b'An account is already registered for that email address.' in response1.data


    def test_signup_incorrect_dob(self, client):
        """
        GIVEN A user is not registered
        WHEN they submit a registration form with an invalid date if birth
        THEN the page should be reloaded and there shouldn't be a record in the user table in the database and a warning
        message should appear
        """

        count = User.query.count()
        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '25/04/2000',
                                        email='test_signup@gmail.com', password='password2', password_confirm='password2'),
                                        follow_redirects=True)
        count2 = User.query.count()
        assert count2 - count == 0      #user not saved in the database because of invalid dob
        assert response.status_code == 200
        assert b'Not a valid date value' in response.data


    def test_signup_future_dob(self, client):
        """
        GIVEN A user is not registered
        WHEN they submit a registration form with a date of birth in the future (after the current day when te signup happens)
        THEN the page should be reloaded and there shouldn't be a record in the user table in the database and a warning
        message should appear
        """

        count = User.query.count()
        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2100-04-25',
                                        email='test_signup@gmail.com', password='password2', password_confirm='password2'),
                                        follow_redirects=True)
        count2 = User.query.count()
        assert count2 - count == 0      #user not saved in the database because of invalid dob
        assert response.status_code == 200
        assert b'Date of Birth must be in the past' in response.data


    def test_signup_different_passwords(self, client):
        """
        GIVEN A user is not registered
        WHEN they submit a registration different passwords
        THEN the page should be reloaded and there shouldn't be a record in the user table in the database and a warning
        message should appear
        """

        count = User.query.count()
        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '25/04/2000',
                                        email='test_signup@gmail.com', password='password1', password_confirm='password2'),
                                        follow_redirects=True)
        count2 = User.query.count()
        assert count2 - count == 0          #user not saved in the database because of not matching passwords
        assert response.status_code == 200
        assert b'Passwords must match' in response.data