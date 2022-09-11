import os
from dotenv import load_dotenv
import re

from binance import Binance


def show_data():
    if data['status']:
        for dictionary in [data, tokens]:
            del dictionary['status']
            for key, value in dictionary.items():
                print(f'{key}: {value}')
    else:
        print('POST запрос не прошел.')
        for key, value in tokens.items():
            print(f'{key}: {value}')


load_dotenv()

email = os.getenv('email')
password = os.getenv('password')
proxy = os.getenv('proxy')

account = Binance(email, password, proxy)
tokens = account.auth()
if tokens['status']:
    data = account.get_name(tokens, proxy)
    show_data()
else:
    print('Selenium не обнаружил запрос "auth".')
account.tear_down()
config = []
with open(".env", "r") as file:
    for line in file:
        if 'p20t' in line:
            line = re.sub(r"p20t=web.\d+\.\w+", f'p20t={tokens["p20t_token"]}', line)
        elif 'csrf' in line:
            line = re.sub(r"csrf=\w+", f'csrf={tokens["csrf_token"]}', line)
        config.append(line)

with open(".env", "w") as file:
    for line in config:
        file.writelines(line)
