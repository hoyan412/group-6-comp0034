# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Authors: Rayan Souissi


from flask_app.models import Posts, Likes, Profile


class TestCommunityShowPost:

    def test_show_specific_post_not_logged_in(self, client):
        """
        GIVEN The user is not logged in
        WHEN a post page is requested
        THEN check that the user does not have access to the page and is redirected to the log in page
        """

        response = client.get('/community/18', follow_redirects=True)   #18 is an existing post id
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data


    def test_show_specific_post_logged_in_without_profile(self, client, user):
        """
        GIVEN The user is logged in
        WHEN a post page is requested
        THEN check that the user have access to the page
        """

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='FN_test',  password="password"), follow_redirects=True)

        response2 = client.get('/community/18', follow_redirects=True)  #18 is an existing post id

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        #assert b'You must create a profile to access the community' in response2.data


    def test_show_specific_post_page_succeeds(self, client, user):
        """
        GIVEN The user is logged in and has a profile
        WHEN a post page is requested
        THEN check that the user has access to the page
        """

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

        response3 = client.get('/community/18', follow_redirects=True) #18 is an existing post id

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200



class TestCommunityCreatePost:

    def test_create_post_not_logged_in(self, client):
        """
        GIVEN The user is not logged in
        WHEN the create post page is requested
        THEN check that the user does not have access to the page and is redirected to the log in page
        """

        response = client.get('/community/create_post', follow_redirects=True)
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data


    def test_create_post_logged_in_without_profile(self, client, user):
        """
        GIVEN The user is logged in but does't have a profile
        WHEN the create post page is requested
        THEN check that the user have access to the page
        """

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='FN_test',  password="password"), follow_redirects=True)

        response2 = client.get('/community/create_post', follow_redirects=True)

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        #assert b'You must create a profile to access the community' in response2.data


    def test_create_post_page_succeeds(self, client, user):
            """
            GIVEN The user is logged in and has a profile
            WHEN the create post page is requested
            THEN check that the user has access to the page
            """

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

            response3 = client.get('/community/create_post')    #no redirection

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert response3.status_code == 200


    def test_create_post_valid(self, client, user):
            """
            GIVEN The user is logged in and has a profile
            WHEN the create post page is posted with a valid title and post
            THEN check that the post is saved in the database
            """

            count = Posts.query.count()

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

            response3 = client.post('/community/create_post', data=dict(post_title='title_test', post='post_test'), follow_redirects=True)

            response4 = client.get('/community/{}'.format(count+1), follow_redirects=True)   #routes to the last post created

            count1 = Posts.query.count()

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert response3.status_code == 200
            assert response4.status_code == 200
            assert b'Your post is now live!' in response3.data
            assert count1-count == 1    #post was saved in the database because both post text and title were provided


    def test_create_post_just_title(self, client, user):
            """
            GIVEN The user is logged in and has a profile
            WHEN the create post page is posted with only a title (no post)
            THEN check that the post is not saved in the database
            """

            count = Posts.query.count()

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

            response3 = client.post('/community/create_post', data=dict(post_title='title_test'), follow_redirects=True)

            count1 = Posts.query.count()

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert response3.status_code == 200
            assert count1-count == 0    #post isn't saved in the database because post text wasn't provided


    def test_create_post_just_post(self, client, user):
            """
            GIVEN The user is logged in and has a profile
            WHEN the create post page is posted with only a post (no title)
            THEN check that the post is not saved in the database
            """

            count = Posts.query.count()

            response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

            #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
            response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

            response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

            response3 = client.post('/community/create_post', data=dict(post='post_test'), follow_redirects=True)

            count1 = Posts.query.count()

            assert response.status_code == 200
            assert response1.status_code == 200
            assert response2.status_code == 200
            assert response3.status_code == 200
            assert count1-count == 0    #post isn't saved in the database because post title wasn't provided


class TestCommunityEditPost:

    def test_edit_post_not_logged_in(self, client):
        """
        GIVEN The user is not logged in
        WHEN the a edit post page is requested
        THEN check that the user does not have access to the page and is redirected to the log in page
        """

        response = client.get('/community/1/edit_post', follow_redirects=True) #1 is an existing post id
        assert response.status_code == 200
        assert b'You must be logged in to view that page.' in response.data


    def test_edit_post_logged_in_without_profile(self, client, user):
        """
        GIVEN The user is logged in but doesnt have a profile
        WHEN the edit post page is requested
        THEN check that the user have access to the page
        """

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='FN_test',  password="password"), follow_redirects=True)

        response2 = client.get('/community/1/edit_post', follow_redirects=True) #1 is an existing post id

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        #assert b'You must create a profile to access the community' in response2.data


    def test_edit_post_page_succeeds(self, client, user):
        """
        GIVEN The user is logged in and has a profile
        WHEN the edit post page is requested
        THEN check that the user has access to the page
        """

        count = Posts.query.count()

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

        response3 = client.post('/community/create_post', data=dict(post_title='title_test', post='post_test'), follow_redirects=True)

        response4 = client.get('/community/{}/edit_post'.format(count+1))   #routes to the last post created    #no redirection


        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200


    def test_edit_post_valid_form(self, client, user):
        """
        GIVEN The user is logged in and has a profile
        WHEN the edit post page is posted with a valid title and post
        THEN check that the post is not saved in the database
        """
        count = Posts.query.count()

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
            email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

        response3 = client.post('/community/create_post', data=dict(post_title='title_test', post='post_test'), follow_redirects=True)

        response4 = client.post('/community/{}/edit_post'.format(count+1), data=dict(post_title='title_test1', post='post_test1'), follow_redirects=True)

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert b'Your post is now live' in response3.data
        assert Posts.query.filter_by(title='title_test1', body='post_test1') != None


    def test_edit_post_just_title(self, client, user):
        """
        GIVEN The user is logged in and has a profile
        WHEN the edit post page is posted with only a title (no post)
        THEN check that the post is not saved in the database
        """
        count = Posts.query.count()

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
            email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

        response3 = client.post('/community/create_post', data=dict(post_title='title_test', post='post_test'), follow_redirects=True)

        response4 = client.post('/community/{}/edit_post'.format(count+1), data=dict(post_title='title_test2')) #no redirection

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert Posts.query.filter_by(title='title_test2') == None


    def test_edit_post_just_post_text(self, client, user):
        """
        GIVEN The user is logged in and has a profile
        WHEN the edit post page is posted with only a post text (no title)
        THEN check that the post is not saved in the database
        """
        count = Posts.query.count()

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
            email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)

        response3 = client.post('/community/create_post', data=dict(post_title='title_test', post='post_test'), follow_redirects=True)

        response4 = client.post('/community/{}/edit_post'.format(count+1), data=dict(post='post_test3'), follow_redirects=True)

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert Posts.query.filter_by(body='post_test3') == None


class TestCommunityLikePost:


    def test_like_post_succeeds(self, client, user):
        """
        GIVEN The user is logged in, has a profile and a valid post page is requested
        WHEN the like button is pressed
        THEN check that the post and profile who liked have 1 more like attributed to them
        """

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        profile_number = Profile.query.count()

        response3 = client.post('/community/create_post', data=dict(post_title='title_test', post='post_test'), follow_redirects=True)
        post_number = Posts.query.count()

        post_like_count = Likes.query.filter_by(post_id=post_number).count()
        profile_like_count = Likes.query.filter_by(profile_id=profile_number).count()

        response4 = client.post('/community/{}/like_post'.format(post_number), follow_redirects=True)

        post_like_count1 = Likes.query.filter_by(post_id=post_number).count()
        profile_like_count1 = Likes.query.filter_by(profile_id=profile_number).count()

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert post_like_count1-post_like_count == 1
        assert profile_like_count1-profile_like_count == 1


    def test_unlike_post_succeeds(self, client, user):
        """
        GIVEN The user is logged in, has a profile, a valid post page is requested, and the post is liked
        WHEN the unlike button is pressed
        THEN check that the post and profile who unliked have 1 les like attributed to them
        """

        response = client.post('signup', data=dict(first_name='FN_test', last_name='LN_test', dob= '2000-04-25',
                email='fn.ln@test.com', password='password', password_confirm = "password"), follow_redirects=True)

        #response1 = client.post('/login', data=dict(email=user.email,  password=user.password), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='fn.ln@test.com',  password='password'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='fn_ln',  bio='bio of fn_ln',
                                photo='Default_Account_Image.png', gender="Male"), follow_redirects=True)
        profile_number = Profile.query.count()

        response3 = client.post('/community/create_post', data=dict(post_title='title_test', post='post_test'), follow_redirects=True)
        post_number = Posts.query.count()

        response4 = client.post('/community/{}/like_post'.format(post_number), follow_redirects=True)

        post_like_count = Likes.query.filter_by(post_id=post_number).count()
        profile_like_count = Likes.query.filter_by(profile_id=profile_number).count()

        response5 = client.post('/community/{}/unlike_post'.format(post_number), follow_redirects=True)

        post_like_count1 = Likes.query.filter_by(post_id=post_number).count()
        profile_like_count1 = Likes.query.filter_by(profile_id=profile_number).count()

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200
        assert post_like_count-post_like_count1 == 1
        assert profile_like_count-profile_like_count1 == 1
