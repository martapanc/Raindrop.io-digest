import os
import urllib.parse as urlparse
from urllib.parse import parse_qs

import redis
import requests
from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Raindrops import collections, add_collection, add_bookmarks

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_URL = "https://raindrop.io/oauth/"
AUTH = "{}authorize?redirect_uri=http://localhost:5000&client_id={}".format(BASE_URL, os.getenv('RAINDROP_CLIENT_ID'))

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


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
    url = 'https://raindrop.io/oauth/access_token'
    payload = {
        'code': obtain_code(),
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

    r.set('access_token', access_token)
    r.set('refresh_token', response_body['refresh_token'])

    return access_token


def get_collections():
    url = "https://api.raindrop.io/rest/v1/collections"

    saved_access_token = r.get('access_token')
    access_token = saved_access_token if saved_access_token else obtain_token()

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    collections_rs = requests.get(url, headers=headers).json()
    if collections_rs['items']:
        for coll in collections_rs['items']:
            add_collection(coll)
    elif collections_rs['errorMessage']:
        obtain_token()
        get_collections()


def get_bookmarks():
    for coll_id, coll in collections.items():
        url = "https://api.raindrop.io/rest/v1/raindrops/{}".format(coll_id)

        saved_access_token = r.get('access_token')
        access_token = saved_access_token if saved_access_token else obtain_token()

        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        raindrops_rs = requests.get(url, headers=headers).json()
        add_bookmarks(coll_id, raindrops_rs['items'])


if __name__ == '__main__':
    get_collections()
    get_bookmarks()
