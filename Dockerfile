FROM python:3.5
MAINTAINER Shohei Miyashita <shohei.miyashita.212@gmail.com>

ADD ./ /root

EXPOSE 8080

WORKDIR /root

RUN python setup.py install

ENV BOTTLE_HOST 0.0.0.0

CMD ["python", "web.py"]