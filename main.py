import os
import urllib.parse as urlparse
from urllib.parse import parse_qs

import requests
from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db_manager import save_token, save_auth_code

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_URL = "https://raindrop.io/oauth/"
AUTH = "{}authorize?redirect_uri=http://localhost:5000&client_id={}".format(BASE_URL, os.getenv('RAINDROP_CLIENT_ID'))


def obtain_code():
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
        auth_code = parse_qs(url.query)['code'][0]
        return auth_code

    except TimeoutError:
        print("Page took too long to load")


def obtain_token():
    auth_code = obtain_code()
    save_auth_code(auth_code)

    url = 'https://raindrop.io/oauth/access_token'
    payload = {
        'code': auth_code,
        # 'code': os.getenv('RAINDROP_CODE'),
        'client_id': os.getenv('RAINDROP_CLIENT_ID'),
        'client_secret': os.getenv('RAINDROP_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:5000',
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    token_rs = requests.post(url, headers=headers, data=payload)

    response_body = token_rs.json()
    access_token = response_body['access_token']
    save_token(access_token, response_body['refresh_token'])
    return access_token


def get_collections():
    url = "https://api.raindrop.io/rest/v1/collections"
    headers = {
        'Authorization': 'Bearer {}'.format(obtain_token())
    }
    collections_rs = requests.get(url, headers=headers)
    for coll in collections_rs.json()['items']:
        print('"{}" - created on {} - last updated on {}'.format(coll['title'], coll['created'], coll['lastUpdate']))


if __name__ == '__main__':
    get_collections()
