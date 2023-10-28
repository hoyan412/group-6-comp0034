# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Youssef Alaoui, Ho Yan Or

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures('chrome_driver', 'selenium')

class TestNavigationHome:

    def test_nav_about(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('nav-about').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/about"

    def test_nav_community_before_login(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('nav-comm').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/login"


    def test_nav_uk_data(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('nav-dash').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/dash_html/"

    def test_login_button(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('login-btn').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/login"

    def test_signup_button(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('signup-btn').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/signup"

    def test_sign_up_now_button(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('signupnow-btn').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/signup"

    # def test_signup(self,app):
    #     self.driver.implicitly_wait(10)
    #     self.driver.get("http://127.0.0.1:5000/signup")
    #     self.driver.find_element_by_id("first_name").send_keys('Test')
    #     self.driver.find_element_by_id("last_name").send_keys('Test')
    #     self.driver.find_element_by_id('dob').send_keys('01012000')
    #     self.driver.find_element_by_id('email').send_keys('test@gmail.com')
    #     self.driver.find_element_by_id('password').send_keys('test')
    #     self.driver.find_element_by_id('password_confirm').send_keys('test')
    #     self.driver.implicitly_wait(10)
    #     WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click"))).click()
    #     self.driver.implicitly_wait(10)
    #     assert self.driver.current_url == "http://127.0.0.1:5000/login"
    def test_login_success(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/login")
        email = 'selenium_18@test.com'
        password = 'password_test'
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_1"))).click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/user.firstname"

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "userhome")))
        message = self.driver.find_element_by_id("userhome").text
        assert message == 'Welcome First Name!'



    def test_about_link(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('abt-link').click()
        assert self.driver.current_url == "http://127.0.0.1:5000/about"

    def test_nav_community(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('nav-comm').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/create_profile"
        username = "My_username1"
        bio = "My_bio"
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("bio").send_keys(bio)
        self.driver.find_element_by_id("gender-0").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('save-click').click()
        self.driver.implicitly_wait(10)

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/display_profile/{}/?url=%2Fstatic%2FDefault_Account_Image.png".format(
            username)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('nav-comm').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/community/"


    def test_connect_link(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('con-link').click()
        assert self.driver.current_url == "http://127.0.0.1:5000/community/"

    def test_visualise_link(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('vis-link').click()
        assert self.driver.current_url == "http://127.0.0.1:5000/dash_html/"

    def test_search_bar(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.find_element_by_id("search-bar").send_keys('My_username1')
        self.driver.find_element_by_id('search-btn').click()
        assert self.driver.current_url == "http://127.0.0.1:5000/community/search_results"


    def test_dd_profile(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.find_element_by_id('dd').click()
        self.driver.find_element_by_id('dd-prof').click()
        username = "My_username1"
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/display_profile/{}/?url=%2Fstatic%2FDefault_Account_Image.png".format(
            username)

    def test_delete_profile(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/delete_profile")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("yes-click").click()
        self.driver.implicitly_wait(10)

        assert self.driver.current_url == 'http://127.0.0.1:5000/'

        self.driver.get("http://127.0.0.1:5000/community")

        assert self.driver.current_url == 'http://127.0.0.1:5000/Profile_and_Account/create_profile'

    def test_dd_account(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.find_element_by_id('dd').click()
        self.driver.find_element_by_id('dd-acc').click()
        username = "My_username1"
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_dd_logout(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.find_element_by_id('dd').click()
        self.driver.find_element_by_id('dd-logout').click()
        assert self.driver.current_url == "http://127.0.0.1:5000/"
        self.driver.get("http://127.0.0.1:5000/community")
        assert self.driver.current_url == "http://127.0.0.1:5000/login"

