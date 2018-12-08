# TelNot
TelegramNotifier - Send Telegram messages easily using HTTP

TelNot is written in Python 3 and it is using Flask (HTTP endpoint) and python-telegram-bot for talking to Telegram service. It is also recommended to be used together with Apache and mod_ssl so the traffic is encrypted using HTTPS (config snipped is avaialble at the end of this README file).

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


### Appendix

#### Using HTTPd as SSL reverse proxy
```
Listen localhost:443 https

<VirtualHost _default_:443>
  SSLCertificateFile /etc/letsencrypt/live/.../fullchain.pem
  SSLCertificateKeyFile /etc/letsencrypt/live/.../privkey.pem

  <Location "/notify">
    ProxyPass http://localhost:5000/notify
    ProxyPassReverse http://localhost:5000/notify
  </Location>
</VirtualHost>                                  
```
