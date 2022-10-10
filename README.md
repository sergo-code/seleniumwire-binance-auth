# seleniumwire-binance-auth
Authorization on the [Binance](https://www.binance.com/) website, in the process it is necessary to manually solve the captcha on the website, then enter two-factor authentication codes in the console.
Output of the following user data: name, id, csrf and p20t.


## Installation
### Dependencies
```
pip install -r requirements.txt
```  
### Rename  
```
mv .env_pub .env
```
### Configuration
```
EMAIL=name@email.com
PASSWORD=qwerty123
PROXY=https://login:password@ip:port
```

### Chromedriver
Select browser version, operating system and download [chromedriver](https://chromedriver.storage.googleapis.com/index.html).  
Put it in the root of the directory.

## Usage
```
python3 main.py
```
