# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Authors: Rayan Souissi
# WARNING RUN THOSE TESTS WHILE MAKING SURE YOU'RE NOT LOGGED IN, IN THE APPLICATION


class TestLogin:

    def test_login_succeeds(self, client, user):
        """
        GIVEN a user is registered
        WHEN they submit a valid login form
        THEN they  should be redirected the home page"
        """

        response = client.post('/login', data=dict(email=user.email,  password=user.password, remember=True), follow_redirects=True)

        assert response.status_code == 200


    def test_login_remember_false(self, client, user):
        """
        GIVEN a user is registred
        WHEN they submit a valid login form without checking the remember me field
        THEN they should be redirected the home page
        """

        response = client.post('/login', data=dict(email=user.email,  password=user.password, remember=True), follow_redirects=True)

        assert response.status_code == 200


    def test_login_with_wrong_password(self, client, user):
        """
        GIVEN A user is not yet registered
        WHEN they submit a login form with a wrong password
        THEN the login page should reloaded and  a message should read "Incorrect password"
        """

        response = client.post('/login', data=dict(email=user.email,  password=user.password +'wrong', remember=True), follow_redirects=True)

        assert response.status_code == 200
        assert b'Incorrect password.' in response.data      #sometimes this doesn't work


    def test_login_with_non_registered_email(self, client):
        """
        GIVEN A user is not yet registered
        WHEN they submit a login form with a non registered email address
        THEN the login page should reload and the a message should read "There is no account registered with this email
        address, please create an account"
        """

        response = client.post('/login', data=dict(email = 'non_registred@test.test',  password='password2', remember=True), follow_redirects=True)

        assert response.status_code == 200
        assert b'There is no account registered with this email address, please create an account' in response.data


