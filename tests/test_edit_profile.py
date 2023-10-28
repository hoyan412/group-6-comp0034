# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Aydan Guliyeva

from flask_app.models import User
from flask_app.models import Profile
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort


class TestEditProfile:

    def test_edit_profile(self, client):
        """
        GIVEN The user has a profile
        WHEN the edit profile page is required
        THEN check that the edit profile page is correctly loaded
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob='2000-04-25',
                                                    email='fn.ln@test.com', password='password',
                                                    password_confirm='password'),
                               follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com', password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln'), follow_redirects=True)

        response3 = client.get('/Profile_and_Account/update_profile')

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200


    def test_edit_profile_succeeds(self, client):
        """
        GIVEN The user is has a profile
        WHEN an edited (username, bio and photo) update profile form is posted
        THEN check that the response is valid and the
        record in the profile table in the database should update
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                                    email='fn.ln@test.com', password='password', password_confirm='password'),
                               follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                                                                 photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        response3 = client.post('/Profile_and_Account/update_profile', data=dict(username='fn_ln1',  bio='bio of fn_ln1',
                                                                            photo='Default_Account_Image1.png', gender="Female"), follow_redirects=True)


        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert Profile.query.filter_by(username='fn_ln1',  bio='bio of fn_ln1', photo='Default_Account_Image1.png', gender="Female") != None

    def test_edit_username(self, client):
        """
        GIVEN The user has a profile
        WHEN an update profile form is posted, editing only username
        THEN check that the response is valid and the new username is recorded
        in the profile table in the database
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                                    email='fn.ln@test.com', password='password', password_confirm='password'),
                               follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                                                                 photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        response3 = client.post('/Profile_and_Account/update_profile', data=dict(username='fn_ln1'), follow_redirects=True)

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert Profile.query.filter_by(username='fn_ln1',  bio='bio of fn_ln1', photo='Default_Account_Image1.png', gender="Female") != None

    def test_edit_username_and_bio(self, client):
        """
        GIVEN The user has a profile
        WHEN an update profile form is posted, editing only username
        THEN check that the response is valid and the new username is recorded
        in the profile table in the database
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                                    email='fn.ln@test.com', password='password', password_confirm='password'),
                               follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                                                                 photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        response3 = client.post('/Profile_and_Account/update_profile', data=dict(username='fn_ln1', bio='bio of fn_ln1'), follow_redirects=True)


        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert Profile.query.filter_by(username='fn_ln1', bio='bio of fn_ln1', photo='Default_Account_Image.png', gender="Male") != None


    def test_edit_bio(self, client):
        """
        GIVEN The user has a profile
        WHEN an update profile form is posted, editing only username
        THEN check that the response is valid and the new username is recorded
        in the profile table in the database
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                                    email='fn.ln@test.com', password='password', password_confirm='password'),
                               follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                                                                 photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        response3 = client.post('/Profile_and_Account/update_profile', data=dict(bio='bio of fn_ln1'), follow_redirects=True)


        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert Profile.query.filter_by(username='fn_ln',  bio='bio of fn_ln1',photo='Default_Account_Image.png', gender="Male") != None


    def test_edit_username_and_photo(self, client):
        """
        GIVEN The user has a profile
        WHEN an update profile form is posted, editing only username
        THEN check that the response is valid and the new username is recorded
        in the profile table in the database
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                                    email='fn.ln@test.com', password='password', password_confirm='password'),
                               follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                                                                 photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        response3 = client.post('/Profile_and_Account/update_profile', data=dict(username='fn_ln1', photo='Default_Account_Imag1.png'), follow_redirects=True)


        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert Profile.query.filter_by(username='fn_ln1',  bio='bio of fn_ln',photo='Default_Account_Imag1.png', gender="Male") != None


    def test_edit_username_and_gender(self, client):
        """
        GIVEN The user has a profile
        WHEN an update profile form is posted, editing only username
        THEN check that the response is valid and the new username is recorded
        in the profile table in the database
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                                                    email='fn.ln@test.com', password='password', password_confirm='password'),
                               follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                                                                 photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        response3 = client.post('/Profile_and_Account/update_profile', data=dict(username='fn_ln1', gender='Prefer not to say'), follow_redirects=True)


        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert Profile.query.filter_by(username='fn_ln1',  bio='bio of fn_ln',photo='Default_Account_Image.png', gender='Prefer not to say') != None


    def test_delete_profile(self, client, user):
        """
        GIVEN The user is logged in and has a profile
        WHEN the delete profile page is requested
        THEN check that the profile was deleted the profile table in the database
        """

        response = client.post('/signup', data=dict(first_name='FN_test', last_name='LN_test', dob='2000-04-25',
                                                    email='fn.ln@test.com', password='password',
                                                    password_confirm='password'),follow_redirects=True)

        response1 = client.post('/login', data=dict(email='fn.ln@test.com', password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln'), follow_redirects=True)

        response3 = client.get('/Profile_and_Account/delete_profile')

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200



