from pages.BinancePage import Binance
from conf import browser, proxy, email, password
from utils import show_data, change_env_config


def binance_auth(browser):
    binance_auth_page = Binance(next(browser))
    binance_auth_page.go_to_site('https://accounts.binance.com/en/login')
    binance_auth_page.enter_email(email())
    binance_auth_page.click_submit()
    binance_auth_page.enter_password(password())
    binance_auth_page.click_submit()
    binance_auth_page.wait_load_page('https://accounts.binance.com/en/confirm-new-device?userType=newYubikey')
    binance_auth_page.click_2fa()
    binance_auth_page.enter_2fa_phone()
    binance_auth_page.enter_2fa_email()
    binance_auth_page.click_2fa_submit()
    binance_auth_page.wait_load_page('https://www.binance.com/en/my/dashboard')
    binance_auth_page.go_to_site('https://binance.com/en')
    tokens = binance_auth_page.get_tokens_auth_request()
    proxies = proxy()
    if proxies != 'None':
        data = binance_auth_page.get_first_name_request(tokens, {'http': proxies})
    else:
        data = binance_auth_page.get_first_name_request(tokens)
    show_data(data, tokens)
    change_env_config(tokens)
    next(browser)


if __name__ == '__main__':
    binance_auth(browser())
