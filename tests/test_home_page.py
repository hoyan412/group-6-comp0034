# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Authors: Rayan Souissi

from flask_app.models import User

class TestHomePage:

    def test_home_page_not_logged_in(self, client):
        """
        GIVEN the Flask application home page and user not logged in
        WHEN the home page is requested
        THEN check that the response is valid
        """

        response = client.get('/')
        assert response.status_code == 200


    def test_home_page_logged_in(self, client, user):
        """
        GIVEN the Flask application home page and user logged in
        WHEN the home page is requested
        THEN check that the response is valid
        """

        response = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.get('/')

        assert response.status_code == 200
        assert response1.status_code == 200