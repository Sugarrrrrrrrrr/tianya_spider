FROM python:3.5 

MAINTAINER Sugar <zhangyushu@live.cn>

RUN rm /etc/apt/sources.list
COPY sources.list /etc/apt/sources.list

RUN apt-get update \
	&& rm /etc/localtime \
	&& ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
	&& mkdir /code

ENV PYTHONIOENCODING=utf-8

WORKDIR /code

RUN pip3 install pymongo requests pyyaml redis scrapy scrapy-redis python-dateutil -i https://mirrors.aliyun.com/pypi/simple/

CMD ["python3", "main_spiders.py"]

