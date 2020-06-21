FROM scrapinghub/scrapinghub-stack-scrapy:2.1

RUN apt-get update
RUN apt-get upgrade -y

RUN echo "es_ES.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN \
 python -m pip install -r /app/requirements.txt --no-cache-dir

RUN pip install -r /app/requirements.txt
COPY . /app
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"