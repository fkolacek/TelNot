# TelNot
TelegramNotifier - Send Telegram messages easily using HTTP

### Usage

1) Install dependencies using pip3
2) Update ``config.ini`` with bot and user definitions
3) Run ``app.py``
4) Profit!

#### Install it
```
$ pip3 install -r requirements.txt 

or 

$ pip3 install flask python-telegram-bot
```

#### Start it
```
$ ./app.py
2018-12-08 22:14:20,084 - root - INFO - Loading bots
2018-12-08 22:14:20,085 - root - INFO - Loading bot: bot1
2018-12-08 22:14:20,085 - root - INFO - Loading bot: bot2
2018-12-08 22:14:20,086 - root - INFO - Starting application
 * Serving Flask app "telnot" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
2018-12-08 22:14:20,095 - werkzeug - INFO -  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

#### Use it
```
$ curl -X POST -d 'token=this-is-very-secret-token' -d 'bot=bot1' -d 'message=testing message 1' 'http://localhost:5000/notify'
```

### License

Released under MIT license, for more information check  LICENSE file.