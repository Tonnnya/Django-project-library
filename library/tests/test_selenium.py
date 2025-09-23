import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import uuid

import os
import django
import sys

library = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '/Users/tonyasmetanina/PycharmProjects/ua-4246-ap-4246-s15-team-5/library')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.library.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
    User.objects.filter(email__startswith="test_").delete()


def generate_unique_email():
    unique_id = uuid.uuid4().hex[:8]
    return f"test_{unique_id}@example.com"


def test_registration(browser):
    email = generate_unique_email()
    password = 'SuperPassword1234'

    browser.get("http://127.0.0.1:8000/")

    browser.find_element(By.ID, "getStarted").click()
    browser.find_element(By.ID, "email").send_keys(email)
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.ID, "password_confirmation").send_keys(password)
    time.sleep(5)

    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    browser.find_element(By.ID, "email").send_keys(email)
    browser.find_element(By.ID, "password").send_keys(password)
    time.sleep(5)

    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


def test_login_incorrect_email(browser):
    browser.get("http://127.0.0.1:8000/auth/login/")

    browser.find_element(By.ID, "email").send_keys('incorrect_email@example.com')
    browser.find_element(By.ID, "password").send_keys("SuperPassword1234")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)

    error_message = browser.find_element(By.CSS_SELECTOR, ".message.error").text
    assert error_message == "Email and/or password are invalid."


def test_login_incorrect_password(browser):
    browser.get("http://127.0.0.1:8000/auth/login/")

    browser.find_element(By.ID, "email").send_keys('tonya@gmail.com')
    browser.find_element(By.ID, "password").send_keys("SuperPassword12345")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(5)

    error_message = browser.find_element(By.CSS_SELECTOR, ".message.error").text
    assert error_message == "Email and/or password are invalid."


def test_login_full_circle(browser):
    VALID_EMAIL = 'tonya@gmail.com'
    VALID_PASSWORD = 'SuperPassword1234'
    INVALID_EMAIL = 'invalid_email@test4.com'
    INVALID_PASSWORD = 'SuperPassword12345'

    browser.get("http://127.0.0.1:8000/")

    login_button = browser.find_element(By.ID, "signIn")
    login_button.click()
    time.sleep(2)

    browser.find_element(By.ID, "email").send_keys(VALID_EMAIL)
    browser.find_element(By.ID, "password").send_keys(VALID_PASSWORD)

    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    browser.find_element(By.ID, "logout").click()
    time.sleep(3)

    email_field = browser.find_element(By.ID, "email")
    assert email_field.is_displayed()

    browser.find_element(By.ID, "email").send_keys(INVALID_EMAIL)
    browser.find_element(By.ID, "password").send_keys(INVALID_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

    error_message = browser.find_element(By.CSS_SELECTOR, ".message.error")
    assert error_message.text == "Email and/or password are invalid."
