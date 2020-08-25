from dotenv import load_dotenv
from pathlib import Path
from selenium import webdriver

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


def obtain_token():
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://raindrop.io/oauth/authorize?redirect_uri=http://localhost:5000&client_id=5f4573de41aff2d4a6774fa2")
    button = driver.find_element_by_id('submit')
    button.click()
    print(driver.current_url)
    pass


if __name__ == '__main__':
    obtain_token()

