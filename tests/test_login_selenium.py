# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Bailey Roberts -

import pytest
from flask_login import current_user
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from flask_app.models import Profile, User


@pytest.mark.usefixtures('chrome_driver', 'selenium')

class TestLoginSelenium:

    #before testing, make sure a user and an account are in the database, using the email bailey_test@gmail.com

    def test_login_success(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/login")
        email = 'selenium_18@test.com'
        password =  'password_test'
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_1"))).click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/user.firstname"

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "userhome")))
        message = self.driver.find_element_by_id("userhome").text
        assert message == 'Welcome First Name!'

    #The first test has logged us in, therefore we want to logout for the next tests
    #We also need to test the logout function
    def test_create_profile(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/create_profile")
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

    def test_modify_username(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/update_profile")

        new_username = "New_username"
        username = self.driver.find_element_by_id("username")
        assert username.text != new_username
        self.driver.execute_script("arguments[0].value = ''", username)
        self.driver.find_element_by_id("username").send_keys(new_username)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('save-click').click()
        self.driver.implicitly_wait(10)

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/display_profile/{}/" \
                                          "?url=%2Fstatic%2FDefault_Account_Image.png".format(
            new_username)

    def test_modify_bio(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/update_profile")

        username = "New_username"
        new_bio = "NewBio"
        bio = self.driver.find_element_by_id("bio")
        assert bio.text != new_bio
        self.driver.execute_script("arguments[0].value = ''", bio)
        self.driver.find_element_by_id("bio").send_keys(new_bio)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('save-click').click()
        self.driver.implicitly_wait(10)

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/display_profile/{}/" \
                                          "?url=%2Fstatic%2FDefault_Account_Image.png".format(
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


    def test_logout(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_class_name("dropdown").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_link_text("Logout").click()
        assert self.driver.current_url == "http://127.0.0.1:5000/"






