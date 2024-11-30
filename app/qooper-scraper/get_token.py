import os
import sys
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import BaseWebDriver
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv

load_dotenv()


QOOPER_HOME_PAGE = "https://mentoring.qooper.io/"

try:
    CHROME_DRIVER_PATH = os.environ.get(
        "CHROME_DRIVER_PATH", r"chromedriver-linux64/chromedriver"
    )
    CHROME_PATH = os.environ.get("CHROME_PATH", r"/usr/bin/google-chrome")
    QOOPER_EMAIL = os.environ["QOOPER_EMAIL"]
    QOOPER_PASSWORD = os.environ["QOOPER_PASSWORD"]
except KeyError as error:
    print(f"Set environment variables: {error.with_traceback()}")
    sys.exit(1)


def wait_for_element_visible(
    driver: BaseWebDriver, element_identifier, by: By = By.XPATH, timeout=10
):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, element_identifier))
    )


def wait_for_element_clickable(
    driver: BaseWebDriver, element_identifier, by: By = By.XPATH, timeout=10
):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, element_identifier))
    )


def login_to_qooper(driver: webdriver.Chrome):
    driver.get(QOOPER_HOME_PAGE)

    input_email = wait_for_element_visible(
        driver,
        "input[type=email]",
        By.CSS_SELECTOR,
    )
    input_email.send_keys(QOOPER_EMAIL)
    next_button = driver.find_element(By.CSS_SELECTOR, "button.btn.bg-blue")
    next_button.click()

    input_password = wait_for_element_visible(
        driver,
        "input[type=password]",
        By.CSS_SELECTOR,
    )
    input_password.send_keys(QOOPER_PASSWORD)
    next_button = driver.find_element(By.CSS_SELECTOR, "button.btn.bg-blue")
    next_button.click()

    radio_input_kagglex = wait_for_element_clickable(
        driver,
        'label[for="KaggleX Fellowship Program - Cohort 4"]',
        By.CSS_SELECTOR,
        timeout=30,
    )

    radio_input_kagglex.click()
    next_button = driver.find_element(By.CSS_SELECTOR, 'button[label="Continue"]')
    next_button.click()

    wait_for_element_visible(
        driver,
        "p",
        By.TAG_NAME,
    )

    auth_token = driver.execute_script("return localStorage.getItem('qooper_atfu');")
    auth_token = json.loads(auth_token)
    print('Auth token: ', f"{auth_token[:4]}...{auth_token[-4:]}")
    with open('qooper-token.txt', 'w') as f:
        f.write(auth_token)


options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"
options.add_argument("--no-sandbox")
service = Service(executable_path=CHROME_DRIVER_PATH)

browser = webdriver.Chrome(
    options=options,
    service=service,
)

try:
    login_to_qooper(browser)

finally:
    browser.quit()

