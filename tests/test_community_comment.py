# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Ho Yan Or

from flask_app.models import Posts, Comments, Comment_Likes

class TestCommunityComment:
    def test_create_comment_no_profile(self, client, user):
        """
        GIVEN The user is logged in with no profile
        WHEN the user successfully writes a comment on a post
        THEN check that the user is redirected to the post and comment is displayed
        """
        response = client.post('signup', data=dict(first_name='test', last_name='test', dob='2000-04-12',
                                                   email='test@gmail.com', password='test',
                                                   password_confirm="test"), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)
        post_number = Posts.query.count()
        response2 = client.post('/community/{}/post_comment'.format(post_number), data=dict(comment='test_comment'),
                                follow_redirects=True)
        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert b'You must create a profile to access the community.' in response2.data

    def test_create_comment_succeeds(self, client, user):
        """
        GIVEN The user with a profile is logged in
        WHEN the user successfully writes a comment on a post
        THEN check that the user is redirected to the post and comment is displayed
        """
        response = client.post('signup', data=dict(first_name='test', last_name='test', dob='2000-04-12',
                                                   email='test@gmail.com', password='test',
                                                   password_confirm="test"), follow_redirects=True)

        response1 = client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)


        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='test', bio='bio of fn_ln',
                                                                                 photo='Default_Account_Image.png',
                                                                                 gender='Female'),follow_redirects=True)
        response3 = client.post('/community/create_post', data=dict(post_title='test', post='test'), follow_redirects=True)
        post_number = Posts.query.count()
        response4 = client.post('/community/{}/post_comment'.format(post_number), data=dict(comment='test_comment'),
                                follow_redirects=True)

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200


    def test_new_comment_valid(self, client, user):
        """
                GIVEN The user with a profile is logged in
                WHEN the user successfully writes a comment on a post
                THEN check that the comment is saved as a new entry in the database
                """
        response = client.post('signup', data=dict(first_name='test', last_name='test', dob='2000-04-12',
                                                   email='test@gmail.com', password='test',
                                                   password_confirm="test"), follow_redirects=True)

        response1 = client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='test', bio = 'hi',
                                                                                 photo = 'Default_Account_Image.png',
                                                                                 gender='Female'),follow_redirects=True)
        response3 = client.post('/community/create_post', data=dict(post_title='test', post='test'),
                                follow_redirects=True)
        post_number = Posts.query.count()
        count = Comments.query.count()
        response4 = client.post('/community/{}/post_comment'.format(post_number), data=dict(comment='test_comment'),
                                follow_redirects=True)
        count1 = Comments.query.count()

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert count1 - count == 1

    def test_edit_comment_succeed(self, client, user):
        """
                GIVEN The user with a profile is logged in and has posted a comment
                WHEN the user edits their comment
                THEN check that the user is redirected to the post and comment is displayed
                """
        response = client.post('signup', data=dict(first_name='test', last_name='test', dob='2000-04-12',
                                                   email='test@gmail.com', password='test',
                                                   password_confirm="test"), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)
        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='test', gender='Female'),
                                follow_redirects=True)
        response3 = client.post('/community/create_post', data=dict(post_title='test', post='test'),
                                follow_redirects=True)
        post_number = Posts.query.count()
        response4 = client.post('/community/{}/post_comment'.format(post_number), data=dict(comment='test_comment'),
                                follow_redirects=True)
        comment_number = Comments.query.count()
        response5 = client.post('/community/{}/{}/edit_comment'.format(post_number, comment_number),
                                data=dict(comment='test_edit_comment'), follow_redirects=True)

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200

    def test_edit_comment_valid(self, client, user):
        """
         GIVEN The user is logged in and has written a comment
         WHEN the user successfully edits their comment on a post
         THEN check that the database entry is updated and that it is not saved as a new entry
         """

        response = client.post('signup', data=dict(first_name='test', last_name='test', dob='2000-04-12',
                                                   email='test@gmail.com', password='test',
                                                   password_confirm="test"), follow_redirects=True)
        response1 = client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)
        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='test', gender='Female'), follow_redirects=True)
        response3 = client.post('/community/create_post', data=dict(post_title='test', post='test'),
                               follow_redirects=True)
        post_number = Posts.query.count()
        response4 = client.post('/community/{}/post_comment'.format(post_number), data=dict(comment='test_comment'),
                               follow_redirects=True)
        comment_count = Comments.query.count()
        response5 = client.post('/community/{}/{}/edit_comment'.format(post_number, comment_count),
                                data=dict(comment='test_edit_comment'), follow_redirects=True)
        comment_count1 = Comments.query.count()

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200
        assert comment_count1 - comment_count == 0

    def test_like_comment(self, client, user):
        """
         GIVEN The user is logged in and is viewing a specific post
         WHEN the user hits the like button for a specific comment
         THEN check that the like count on the comment increases by 1
            and display - You have liked this comment
         """
        count = Comment_Likes.query.count()
        response = client.post('signup', data=dict(first_name='test', last_name='test', dob='2000-04-12',
                                                   email='test@gmail.com', password='test',
                                                   password_confirm="test"), follow_redirects=True)

        response1 = client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='test', bio = 'hi',
                                                                                 photo = 'Default_Account_Image.png',
                                                                                 gender='Female'),follow_redirects=True)
        response3 = client.post('/community/create_post', data=dict(post_title='test', post='test'),
                                follow_redirects=True)
        post_number = Posts.query.count()
        response4 = client.post('/community/{}/post_comment'.format(post_number), data=dict(comment='test_comment'),
                                follow_redirects=True)
        comment_number = Comments.query.count()
        response5 = client.post('/community/{}/{}/like_comment'.format(post_number, comment_number), follow_redirects=True)

        count1 = Comment_Likes.query.count()

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200
        assert count1-count == 1

    def test_unlike_comment(self, client, user):
        """
         GIVEN The user is logged in and has liked a specific comment
         WHEN the user hits the unlike button for that comment
         THEN check that the like count on the comment reduces by 1
            and display - You have unliked this comment
         """
        response = client.post('signup', data=dict(first_name='test', last_name='test', dob='2000-04-12',
                                                   email='test@gmail.com', password='test',
                                                   password_confirm="test"), follow_redirects=True)

        response1 = client.post('/login', data=dict(email='test@gmail.com', password='test'), follow_redirects=True)

        response2 = client.post('/Profile_and_Account/create_profile', data=dict(username='test', bio='hi',
                                                                                 photo='Default_Account_Image.png',
                                                                                 gender='Female'),
                                follow_redirects=True)
        response3 = client.post('/community/create_post', data=dict(post_title='test', post='test'),
                                follow_redirects=True)
        post_number = Posts.query.count()
        response4 = client.post('/community/{}/post_comment'.format(post_number), data=dict(comment='test_comment'),
                                follow_redirects=True)
        comment_number = Comments.query.count()
        response5 = client.post('/community/{}/{}/like_comment'.format(post_number, comment_number),
                                follow_redirects=True)
        count = Comment_Likes.query.count()
        response6 = client.post('/community/{}/{}/unlike_comment'.format(post_number, comment_number),
                                follow_redirects=True)
        count1 = Comment_Likes.query.count()

        assert response.status_code == 200
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200
        assert response6.status_code == 200
        assert count1 - count == 1