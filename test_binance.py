from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver

import os
import re
from dotenv import load_dotenv
from time import sleep
import requests
import json
import pytest

load_dotenv()


class TestBinance:
    @pytest.fixture
    def set_up(self):
        self.email = os.getenv('email')
        self.password = os.getenv('password')
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        self.options_wire = {'proxy': {'https': os.getenv('proxy')}}
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options,
                                       seleniumwire_options=self.options_wire)

    def auth(self, set_up):
        url = 'https://accounts.binance.com/ru/login'
        driver = self.driver
        driver.get(url)
        driver.implicitly_wait(20)
        sleep(5)
        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys(self.email)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(self.password)

        password_field.send_keys(Keys.RETURN)
        input('Капча введена, страница с вводом кода открыта? [ENTER]')
        get_2fa = driver.find_elements(By.XPATH, ".//*[@class='bn-input-suffix css-vurnku']/div")
        for item in get_2fa:
            item.click()

        if driver.find_elements(By.CSS_SELECTOR, "[aria-label='Код верификации (на телефон)']"):
            phone_2fa = driver.find_element(By.CSS_SELECTOR, "[aria-label='Код верификации (на телефон)']")
            code_phone = input('Введите код с телефона [123456]: ')
            phone_2fa.send_keys(code_phone)

        if driver.find_elements(By.CSS_SELECTOR, "[aria-label='Код верификации (на эл. почту)']"):
            email_2fa = driver.find_element(By.CSS_SELECTOR, "[aria-label='Код верификации (на эл. почту)']")
            code_email = input('Введите код с почты [123456]: ')
            email_2fa.send_keys(code_email)

        return self._get_tokens_auth()

    def _get_tokens_auth(self):
        url = 'https://binance.com/ru'
        driver = self.driver
        driver.get(url)

        for request in driver.requests:
            if request.url == 'https://www.binance.com/bapi/accounts/v1/public/authcenter/auth':
                if request.response.status_code == 200:
                    print(request.response.headers.get('date'))

                    csrf_token = request.headers.get('csrftoken')
                    cookie = request.headers.get('cookie')
                    p20t_token = re.search(r"(?<=p20t=)web.\d+\.\w+", cookie).group()
                    return dict(csrf_token=csrf_token, p20t_token=p20t_token, status=True)
                else:
                    print(request.response.status_code)
        del driver.requests
        return dict(status=False)

    @staticmethod
    def _create_request(tokens):
        url = 'https://www.binance.com/bapi/accounts/v1/private/account/user/base-detail'
        useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        headers = {'clienttype': 'web',
                   'content-type': 'application/json',
                   'cookie': f'p20t={tokens["p20t_token"]}; lang=en',
                   'csrftoken': tokens["csrf_token"],
                   'user-agent': useragent
                   }
        return url, headers

    @pytest.mark.webtest
    @pytest.mark.parametrize('tokens, proxy', [(dict(csrf_token=os.getenv('csrf'), p20t_token=os.getenv('p20t')),
                                                os.getenv('proxy'))
                                               ]
                             )
    def test_get_name(self, tokens, proxy):
        url, headers = self._create_request(tokens)
        for i in range(5):
            auth_response = requests.post(url=url, headers=headers, proxies={'http': proxy})
            assert auth_response.status_code == 200
            if auth_response:
                if json.loads(auth_response.text)["success"]:
                    first_name = json.loads(auth_response.text)["data"]["firstName"]
                    user_id = json.loads(auth_response.text)["data"]["userId"]
                    print(first_name, user_id)
                    return dict(first_name=first_name, user_id=user_id, status=True)
                elif i == 4:
                    return dict(status=False)
            elif i == 4:
                return dict(status=False)
            sleep(2)

    @pytest.mark.webtest
    def test_tear_down(self, set_up):
        self.driver.close()
