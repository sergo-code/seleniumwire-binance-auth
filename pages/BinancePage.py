from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import re
from time import sleep
import requests
import json

from utils.BaseApp import BasePage


class BinanceAuthLocators:
    LOCATOR_BINANCE_EMAIL_FIELD = (By.NAME, "username")
    LOCATOR_BINANCE_PASSWORD_FIELD = (By.NAME, "password")
    LOCATOR_BINANCE_SUBMIT_BUTTON = (By.ID, "click_login_submit")
    LOCATOR_BINANCE_2FA_FIELD = (By.XPATH, ".//*[@class='bn-input-suffix css-vurnku']/div[@data-bn-type='text']")
    LOCATOR_BINANCE_2FA_PHONE_FIELD = (By.CSS_SELECTOR, "[aria-label='Phone Number Verification Code']")
    LOCATOR_BINANCE_2FA_EMAIL_FIELD = (By.CSS_SELECTOR, "[aria-label='Email Verification Code']")
    LOCATOR_BINANCE_2FA_SUBMIT_BUTTON = (By.XPATH, ".//div[@class='bn-2fa-submit css-vurnku']/button")


class Binance(BasePage):
    def enter_email(self, EMAIL):
        email_field = self.find_element(BinanceAuthLocators.LOCATOR_BINANCE_EMAIL_FIELD)
        email_field.send_keys(EMAIL)

    def enter_password(self, PASSWORD):
        password_field = self.find_element(BinanceAuthLocators.LOCATOR_BINANCE_PASSWORD_FIELD)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)

    def click_submit(self):
        self.find_element(BinanceAuthLocators.LOCATOR_BINANCE_SUBMIT_BUTTON).click()

    def wait_load_page(self, url):
        self.check_url(url)

    def click_2fa(self):
        get_2fa = self.find_elements(BinanceAuthLocators.LOCATOR_BINANCE_2FA_FIELD)
        for item in get_2fa:
            item.click()

    def enter_2fa_phone(self):
        if self.find_elements(BinanceAuthLocators.LOCATOR_BINANCE_2FA_PHONE_FIELD):
            phone_2fa = self.find_element(BinanceAuthLocators.LOCATOR_BINANCE_2FA_PHONE_FIELD)
            code_phone = input('Введите код с телефона [123456]: ')
            phone_2fa.send_keys(code_phone)

    def enter_2fa_email(self):
        if self.find_elements(BinanceAuthLocators.LOCATOR_BINANCE_2FA_EMAIL_FIELD):
            email_2fa = self.find_element(BinanceAuthLocators.LOCATOR_BINANCE_2FA_EMAIL_FIELD)
            code_email = input('Введите код с почты [123456]: ')
            email_2fa.send_keys(code_email)

    def click_2fa_submit(self):
        self.find_element(BinanceAuthLocators.LOCATOR_BINANCE_2FA_SUBMIT_BUTTON).click()

    def get_tokens_auth_request(self):
        for request in self.driver.requests:
            if request.url == 'https://www.binance.com/bapi/accounts/v1/public/authcenter/auth':
                if request.response.status_code == 200:
                    print(request.response.headers.get('date'))

                    csrf_token = request.headers.get('csrftoken')
                    cookie = request.headers.get('cookie')
                    p20t_token = re.search(r"(?<=p20t=)web.\d+\.\w+", cookie).group()
                    return dict(csrf_token=csrf_token, p20t_token=p20t_token, status=True)
                else:
                    print(request.response.status_code)
        del self.driver.requests
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

    def get_first_name_request(self, tokens, proxies=None):
        url, headers = self._create_request(tokens)
        for i in range(5):
            auth_response = requests.post(url=url, headers=headers, proxies=proxies)
            if auth_response:
                if json.loads(auth_response.text)["success"]:
                    first_name = json.loads(auth_response.text)["data"]["firstName"]
                    user_id = json.loads(auth_response.text)["data"]["userId"]
                    return dict(first_name=first_name, user_id=user_id, status=True)
                elif i == 4:
                    return dict(status=False)
            elif i == 4:
                return dict(status=False)
            sleep(2)
