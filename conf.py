import os
from dotenv import load_dotenv

from seleniumwire import webdriver


load_dotenv()


def proxy():
    return os.getenv('PROXY')


def email():
    return os.getenv('EMAIL')


def password():
    return os.getenv('PASSWORD')


def browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    options_wire = {'proxy': {'https': proxy()}}
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options, seleniumwire_options=options_wire)
    return driver
