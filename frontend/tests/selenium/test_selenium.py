import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import random
import string


def test_check_website_title():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.

    # Setup the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the page
        driver.get("http://10.90.137.146:9000/")

        # Assert the title (you need to know the expected title)
        assert "Streamlit" in driver.title

    finally:
        # Close the browser window
        driver.quit()


def test_register_new_user():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.

    # Setup the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    try:
        # Navigate to the registration page
        # Update URL if the path is different
        driver.get("http://10.90.137.146:9000")
        USERNAME = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=30))
        PASSWORD = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=30))

        username_input = driver.find_element(By.ID, "text_input_1")
        username_input.send_keys(USERNAME)

        password_input = driver.find_element(By.ID, "text_input_2")
        password_input.send_keys(PASSWORD)

        # somehow in main page exists 4 or more buttons... [4] - "sign up"
        submit_button = driver.find_elements(By.TAG_NAME, "button")[4]
        submit_button.click()

        success_message = driver.find_element(By.ID, "text_input_3")
        print(success_message)

    finally:
        # Close the browser window
        driver.quit()


def test_log_in_user():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.

    # Setup the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    try:
        # Navigate to the registration page
        # Update URL if the path is different
        driver.get("http://10.90.137.146:9000")

        username_input = driver.find_element(By.ID, "text_input_1")
        username_input.send_keys("1231234")

        password_input = driver.find_element(By.ID, "text_input_2")
        password_input.send_keys("1231234")

        # somehow in main page exists 4 or more buttons... [4] - "sign up"
        submit_button = driver.find_elements(By.TAG_NAME, "button")[3]
        submit_button.click()
        try:
            driver.find_element(By.ID, "text_input_3")
        except NoSuchElementException as e:
            pytest.fail("Log in failed", e)

        elements = driver.find_elements(By.TAG_NAME, 'p')
        for e in elements:
            if e.text == "Add activity":
                # print(e.text)
                e.click()
                break

        activity_input = driver.find_element(By.ID, "text_input_4")
        activity_input.send_keys("selenium_test_bullshit")

        enter_time_input = driver.find_element(By.ID, "text_input_5")
        enter_time_input.send_keys("11:11:11")

        elements = driver.find_elements(By.TAG_NAME, 'p')
        for e in elements:
            if e.text == "Save":
                e.click()
                break

        sleep(2)  # need time to update elements
        elements = driver.find_elements(By.TAG_NAME, 'p')
        # for it in elements:
        # print(it.text)
        assert any(
            it.text == "Saved activity: selenium_test_bullshit, Time: 11:11:11" for it in elements) == True

    finally:
        # Close the browser window
        driver.quit()
