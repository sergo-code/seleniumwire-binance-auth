# seleniumwire-binance-auth
Авторизация на сайте [Binance](https://www.binance.com/), в процессе необходимо вручную решить капчу на сайте, далее в консоли ввести коды двухфакторной аутентификации.
Вывод следующих данных о пользователе: имя, id, csrf и p20t.

```
pip install -r requirements.txt
```  

Переименовать  
.env_pub -> .env  
Добавить данные:
- email
- password
- proxy

Запуск
```
python3 main.py
```
Тестирование
```
pytest -m webtest -v
```
