FROM python:3.5
MAINTAINER Shohei Miyashita <shohei.miyashita.212@gmail.com>

ADD ./ /root

EXPOSE 8080

WORKDIR /root

CMD ['python', 'web.py']