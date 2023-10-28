# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 28/04/2021
# Project: CW 2
# Authors: Youssef Alaoui
#This file needs to be run after test_signup_selenium.py

import pytest
from flask_login import current_user
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from flask_app.models import Profile, User


@pytest.mark.usefixtures('chrome_driver', 'selenium')

class TestLoginSelenium:

    def test_nav_about(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('nav-about').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/about"

    def test_login_success(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/login")
        email = 'selenium_18@test.com'
        password =  'password_test'
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_1"))).click()
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

        #As fixtures don't work, we need to rerun this bit of code using the old password so that it doesn't get stuck

    def test_modify_firstname(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"

        old = self.driver.find_element_by_id('firstname')
        oldfirst = old.get_attribute('placeholder')

        self.driver.find_element_by_id('firstname').send_keys('New First Name')
        assert oldfirst != "New First Name"

        self.driver.find_element_by_id('updatefirstname').click()

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_modify_firstname_back(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"

        old = self.driver.find_element_by_id('firstname')
        oldfirst = old.get_attribute('placeholder')

        self.driver.find_element_by_id('firstname').send_keys('First Name')
        assert oldfirst != "First Name"

        self.driver.find_element_by_id('updatefirstname').click()

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_modify_lastname(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"

        old = self.driver.find_element_by_id('lastname')
        oldlast = old.get_attribute('placeholder')

        self.driver.find_element_by_id('lastname').send_keys('New Last Name')
        self.driver.find_element_by_id('updatelastname').click()
        assert oldlast != "New Last Name"

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_modify_lastname_back(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"

        old = self.driver.find_element_by_id('lastname')
        oldlast = old.get_attribute('placeholder')

        self.driver.find_element_by_id('lastname').send_keys('Last Name')
        self.driver.find_element_by_id('updatelastname').click()
        assert oldlast != "Last Name"

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_modify_email(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"

        old = self.driver.find_element_by_id('email')
        oldemail = old.get_attribute('placeholder')

        self.driver.find_element_by_id('email').send_keys('Newemail@test.test')
        self.driver.find_element_by_id('updateemail').click()

        assert oldemail != "Newemail@test.test"


        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_modify_email_back(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"

        old = self.driver.find_element_by_id('email')
        oldemail = old.get_attribute('placeholder')

        self.driver.find_element_by_id('email').send_keys('selenium_18@test.com')

        self.driver.find_element_by_id('updateemail').click()
        assert oldemail != "selenium_18@test.com"

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_modify_dob(self,app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"

        new_dob = '02022000'
        self.driver.find_element_by_id('dob').send_keys(new_dob)

        self.driver.find_element_by_id('updatedob').click()

        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/user_account"

    def test_modify_password(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"
        self.driver.find_element_by_id("changepasswordbtn").click()

        assert self.driver.current_url == 'http://127.0.0.1:5000/Profile_and_Account/edit_account/password_change'

        new_password = 'new_password'
        self.driver.find_element_by_id('new_password').send_keys(new_password)
        self.driver.find_element_by_id('new_password_confirm').send_keys(new_password)

        self.driver.find_element_by_id("update-click").click()

        assert self.driver.current_url =='http://127.0.0.1:5000/Profile_and_Account/user_account'

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "flash")))
        message = self.driver.find_element_by_id("flash").text
        assert message == 'Password has been updated!'

    def test_modify_password_back(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/Profile_and_Account/user_account")
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("accountbtn").click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/Profile_and_Account/edit_account"
        self.driver.find_element_by_id("changepasswordbtn").click()

        assert self.driver.current_url == 'http://127.0.0.1:5000/Profile_and_Account/edit_account/password_change'

        new_password = 'password_test'
        self.driver.find_element_by_id('new_password').send_keys(new_password)
        self.driver.find_element_by_id('new_password_confirm').send_keys(new_password)

        self.driver.find_element_by_id("update-click").click()

        assert self.driver.current_url =='http://127.0.0.1:5000/Profile_and_Account/user_account'

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "flash")))
        message = self.driver.find_element_by_id("flash").text
        assert message == 'Password has been updated!'



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

    def test_login_fail_email(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/login")
        email = 'incorrect_email@gmail.com'
        password = 'test'
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_1"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/login"

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "error")))
        message = self.driver.find_element_by_id("error").text
        assert message == 'There is no account registered with this email address, please create an account'

    def test_login_fail_password(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/login")
        email = 'selenium_18@test.com'
        password = 'incorrect_password'
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("password").send_keys(password)
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.ID, "click_1"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/login"

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "error")))
        message = self.driver.find_element_by_id("error").text
        assert message == 'Incorrect password.'

    def test_get_to_login_page(self, app): #we are still logged out, from the logout test, all other tests have been unsuccessful
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/login"




