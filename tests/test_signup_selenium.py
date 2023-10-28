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

@pytest.mark.usefixtures('chrome_driver', 'selenium')

class TestSignUpSelenium:

    def test_app_is_running(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        assert self.driver.title == ''

    def test_signup_success(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/signup")
        first_name = 'Test'
        last_name = 'Test'
        dob = '01012000'
        email = 'selenium_18@test.com' #because the testing and the main database are the same, this needs to be changed so that the user can sign up succesfully.
        password = 'password_test'
        password_confirm = 'password_test'
        self.driver.find_element_by_id("first_name").send_keys(first_name)
        self.driver.find_element_by_id("last_name").send_keys(last_name)
        self.driver.find_element_by_id('dob').send_keys(dob)
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password_confirm').send_keys(password_confirm)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('click').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/login"

        message = self.driver.find_element_by_id("flash").text
        assert message == 'Hello, Test. You have successfully registered.'
       # assert f"Hello, {first_name}. You have successfully registered." in message

    def test_signup_fail_password_confirm(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/signup")
        first_name = 'Test'
        last_name = 'Test'
        dob = '01012000'
        email = 'selenium_14@test.com'  # because the testing and the main database are the same, this needs to be changed so that the user can sign up succesfully.
        password = 'password_test'
        password_confirm = 'incorrect_password_test'
        self.driver.find_element_by_id("first_name").send_keys(first_name)
        self.driver.find_element_by_id("last_name").send_keys(last_name)
        self.driver.find_element_by_id('dob').send_keys(dob)
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password_confirm').send_keys(password_confirm)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('click').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/signup"

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "error")))
        message = self.driver.find_element_by_id("error").text
        assert message == 'Passwords must match'
    # assert f"Hello, {first_name}. You have successfully registered." in message


    def test_signup_fail_email(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/signup")
        first_name = 'Test'
        last_name = 'Test'
        dob = '01012000'
        email = 'testa@gmail.com'  # This email is already used in the database.
        password = 'password_test'
        password_confirm = 'password_test'
        self.driver.find_element_by_id("first_name").send_keys(first_name)
        self.driver.find_element_by_id("last_name").send_keys(last_name)
        self.driver.find_element_by_id('dob').send_keys(dob)
        self.driver.find_element_by_id('email').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password_confirm').send_keys(password_confirm)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id('click').click()
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == "http://127.0.0.1:5000/signup"

        WebDriverWait(self.driver, timeout=3).until(EC.visibility_of_element_located((By.ID, "error")))
        message = self.driver.find_element_by_id("error").text
        assert message == 'An account is already registered for that email address.'
        # assert f"Hello, {first_name}. You have successfully registered." in message

    def test_get_to_signup_page(self, app):
        self.driver.implicitly_wait(10)
        self.driver.get("http://127.0.0.1:5000/")
        WebDriverWait(self.driver, timeout=3).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))).click()
        assert self.driver.current_url == "http://127.0.0.1:5000/signup"


