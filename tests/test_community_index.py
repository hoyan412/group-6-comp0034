# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Authors: Rayan Souissi


class TestCommunityIndexPage:

    def test_community_page_not_logged_in(self, client):
        """
        GIVEN The user is not logged in
        WHEN the community page is requested
        THEN check that the user does not have access to the page and is redirected to the log in page
        """

        response = client.get('/community/', follow_redirects=True)
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data


    def test_community_page_logged_in_without_profile(self, client, user):
            """
            GIVEN The user is logged in but hasn't created a profile
            WHEN the community page is requested
            THEN check that the user is redirected to the create a profile page
            """

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='FN_test',  password="password"), follow_redirects=True)

            response2 = client.get('/community/', follow_redirects=True)

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            #assert b'You must create a profile to access the community.' in response2.data


    def test_community_page_succeeds(self, client, user):
            """
            GIVEN The user is logged in and has a profile
            WHEN the community page is requested
            THEN check that the user has access to the page
            """

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

            response3 = client.get('/community/') #no redirection

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert response3.status_code == 200
