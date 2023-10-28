# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Authors: Rayan Souissi - Aydan Guliyeva


from flask_app.models import Profile
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort

class TestCreateProfile:

    def test_create_profile_not_logged_in(self, client):
            """
            GIVEN The user is not logged in
            WHEN the create page is requested
            THEN check that the user does not have access to the page and is redirected to the log in page
            """

            response = client.get('/Profile_and_Account/create_profile', follow_redirects=True)      #redirection to login page

            assert response.status_code == 200
            assert b'You must be logged in to view that page.' in response.data


    def test_create_profile_logged_in(self, client, user):
            """
            GIVEN The user is  logged in
            WHEN the create page is requested
            THEN check that the create page is correctly loaded
            """

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.get('/Profile_and_Account/create_profile')              #no redirection

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200


    def test_create_profile_succeeds(self, client, user):
            """
            GIVEN The user is  logged in
            WHEN a complete (username, bio, photo and gender) create profile form is posted
            THEN check that the response is valid and there should be  a
            record in the profile table in the database
            """

            count = Profile.query.count()

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

            count1 = Profile.query.count()

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert count1-count == 1            #new profile correctly saved in the database


    def test_create_profile_only_username(self, client, user):
            """
            GIVEN The user is  logged in
            WHEN a create profile form is posted, using only the username
            THEN check that the response is valid and there should not be a
            record in the profile table in the database
            """

            count = Profile.query.count()

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln'), follow_redirects=True)

            count1 = Profile.query.count()

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert count1-count == 0                     #new profile not saved in the database because gender wasnt provided
            #assert b'Gender field is required' in response2.data


    def test_create_profile_only_username_and_bio(self, client, user):
            """
            GIVEN The user is  logged in
            WHEN a complete create profile form is posted, using only the username and bio
            THEN check that the response is valid and there should be not be a
            record in the profile table in the database
            """

            count = Profile.query.count()

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln', bio = "bio"), follow_redirects=True)

            count1 = Profile.query.count()

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert count1-count == 0                     #new profile not saved in the database because gender wasnt provided
            #assert b'Gender field is required' in response.data


    def test_create_profile_only_username_bio_and_photo(self, client, user):
            """
            GIVEN The user is  logged in
            WHEN a complete create profile form is posted, using only the username, bio and photo
            THEN check that the response is valid and there should not be a
            record in the profile table in the database
            """

            count = Profile.query.count()

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln', bio = "bio", photo='Default_Account_Image.png'), follow_redirects=True)

            count1 = Profile.query.count()

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert count1-count == 0                    #new profile not saved in the database because gender wasnt provided
            #assert b'Gender field is required' in response.data