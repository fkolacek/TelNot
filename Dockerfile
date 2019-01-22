FROM python:3-slim
LABEL author.name = "František Koláček
LABEL author.url = "https://github.com/fkolacek"

WORKDIR /usr/src/app

COPY requirements.txt .

RUN mkdir -p config && \
  pip3 install -r requirements.txt

ADD telnot/ ./telnot
COPY app.py ./
COPY config.ini.example ./config.ini
CMD /usr/local/bin/python3 app.py
