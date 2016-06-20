FROM python:2.7.10
MAINTAINER Shohei Miyashita <shohei.miyashita.212@gmail.com>

ADD ../ /root

EXPOSE 8080

WORKDIR /root

RUN python -r requirements.txt install

ENV BOTTLE_HOST 0.0.0.0

CMD ["python", "web.py"]