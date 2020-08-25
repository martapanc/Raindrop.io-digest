import os
import urllib.parse as urlparse
from urllib.parse import parse_qs

from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver

# Setup functions to read from .env file
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_URL = "https://raindrop.io/oauth/"
AUTH = "{}authorize?redirect_uri=http://localhost:5000&client_id={}".format(BASE_URL, os.getenv('RAINDROP_CLIENT_ID'))


def obtain_token():
    driver = webdriver.Chrome('./chromedriver')
    driver.get(AUTH)
    delay = 3

    try:
        email_input = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'email')))
        pw_input = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'password')))
        login_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'loginButton')))

        email_input.send_keys(os.getenv('RAINDROP_EMAIL'))
        pw_input.send_keys(os.getenv('RAINDROP_PW'))
        login_button.click()

        button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//input[@type="submit" and @value="Agree"]')))
        button.click()
        url = urlparse.urlparse(driver.current_url)
        param = parse_qs(url.query)['code']
        print(param)
        pass

    except TimeoutError:
        print("Page took too long to load")


if __name__ == '__main__':
    obtain_token()

