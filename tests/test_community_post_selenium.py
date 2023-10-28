# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Bailey Roberts

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

@pytest.mark.usefixtures('chrome_driver', 'selenium')

class TestCommunityPostPage:

    #before testing, make sure a user and an account are in the database, using the email bailey_test@gmail.com


    def test_login_success(self, app): #login to test community functions, this account already has a profile
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/login")
        email = 'bailey_test@gmail.com'
        password =  'test'
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_1"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/user.firstname"

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "userhome")))
        message = self.driver.find_element_by_id("userhome").text
        assert message == 'Welcome Bailey!'

    def test_create_post_page(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/community")
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_2"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/community/create_post"

    def test_create_post(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/community")
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_2"))).click()
        post_title = 'Bailey_Test_Post_1'
        post = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla lacinia leo in arcu porta accumsan at vel nunc. Quisque facilisis elit sit amet dolor pulvinar aliquam. Donec mollis venenatis sem. Maecenas vitae aliquam quam. Nam non vehicula magna. Nunc mollis nibh a augue lacinia, nec aliquam est viverra. Duis vitae sagittis dolor. Phasellus hendrerit eros vel malesuada hendrerit. Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        self.driver.find_element_by_id("post_title").send_keys(post_title)
        self.driver.find_element_by_id("post").send_keys(post)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_3"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/community/?url=http%3A%2F%2F127.0.0.1%3A5000%2F_uploads%2Fphotos%2Fbongo_16.png"
        #Asser that we are redirected to the main coummnity page, with the correct flash message. Because of how the profile picure works, the main community URL is changed.

        message = self.driver.find_element_by_id("flash").text
        assert message == 'Your post is now live!'

    def test_get_post(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/community")
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.CLASS_NAME, "post-title"))).click()
        #This opens up the  first post available
        assert self.driver.current_url == "http://127.0.0.1:5000/community/1"

    def test_like(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/community")
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.CLASS_NAME, "post-title"))).click()
        #This opens up the  first post available
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "like"))).click()
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "unlike")))
        message = self.driver.find_element_by_id("flash").text
        assert message == 'You have liked this post'
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "unlike"))).click()
        #undo the like for later tests

    def test_comment(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/community")
        WebDriverWait(self.driver, timeout=10).until(EC.element_to_be_clickable((By.CLASS_NAME, "post-title"))).click()
        # This opens up the  first post available
        self.driver.implicitly_wait(10)
        #element = self.driver.find_element_by_id("click_5")
        #actions = ActionChains(self.driver)
        #actions.move_to_element(element).perform()
        #WebDriverWait(self.driver, timeout=10).until(EC.element_to_be_clickable((By.ID, 'click_5'))).click()
        #self.driver.find_element_by_id('click_5').click()
        element = self.driver.find_element_by_xpath('//a[contains(@href,"/community/1/post_comment")]')
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(element, 5, 5)
        WebDriverWait(self.driver, timeout=10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href,"/community/1/post_comment")]'))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/community/1/post_comment"

        comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla lacinia leo in arcu porta accumsan at vel nunc. Quisque facilisis elit sit amet dolor pulvinar aliquam. Donec mollis venenatis sem. Maecenas vitae aliquam quam. Nam non vehicula magna. Nunc mollis nibh a augue lacinia, nec aliquam est viverra. Duis vitae sagittis dolor. Phasellus hendrerit eros vel malesuada hendrerit. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.driver.find_element_by_id("comment").send_keys(comment)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_4"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/community/1"

        message = self.driver.find_element_by_id("flash").text
        assert message == 'Your comment is now live!'

        #  I don't know why test_comment doesn't work

    def test_comment_like(self, app):  #This doesn't run if the comment is already liked.
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/community")
        WebDriverWait(self.driver, timeout=10).until(EC.element_to_be_clickable((By.CLASS_NAME, "post-title"))).click()
        # This opens up the  first post available
        self.driver.implicitly_wait(10)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "like_comment"))).click()
        #WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "unlike_comment")))
        assert self.driver.current_url == "http://127.0.0.1:5000/community/1?url=http%3A%2F%2F127.0.0.1%3A5000%2F_uploads%2Fphotos%2Fbongo_16.png"

        message = self.driver.find_element_by_id("flash").text
       # WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "unlike_comment"))).click()
        assert message == 'You have liked this comment'














