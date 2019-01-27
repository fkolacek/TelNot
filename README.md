# TelNot
TelegramNotifier - Send Telegram messages easily using HTTP

TelNot is written in Python 3 and it is using Flask (HTTP endpoint) and python-telegram-bot for talking to Telegram service. It is also recommended to be used together with Apache and mod_ssl so the traffic is encrypted using HTTPS (config snipped is available at the end of this README file).

### Usage

1) Install dependencies using pip3
2) Copy ``config.ini.example`` as ``config.ini`` and update it with bot and user definitions
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

#### Dockerise it

##### Using docker-compose
Just use ``docker-compose build`` to build your own Docker image.

Use ``docker-compose up`` to run it on docker.

Alter `Dockerfile` and `docker-compose.yaml` files in order to meet your own needs.

##### The CLI way
Build it using:
```bash
docker build . -t fkolacek/telnot
```

Create your ``config.ini`` file and then run a daemonised container with:
docker run -d --name telnot -v $PWD/config.ini:/usr/src/app/config.ini -p 5000:5000 fkolacek/telnot

##### Security
There are many ways to run this through Traefik to make it run securely on HTTPS

##### Scalability
One can use ``ConfigMap`` in Kubernetes to provide this service with its ``config.ini`` and set multiple Replicas
